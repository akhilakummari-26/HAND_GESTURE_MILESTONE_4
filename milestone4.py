import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import math
import time
import matplotlib.pyplot as plt
from collections import deque
import platform

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Gesture Volume Control Dashboard", layout="wide")

# -------------------- UI STYLE --------------------
st.markdown("""
<style>

.header{
background:linear-gradient(90deg,#1f77ff,#6a11cb);
padding:15px;
border-radius:10px;
color:white;
font-size:24px;
font-weight:600;
}

.panel{
background:#f8f9fb;
padding:15px;
border-radius:12px;
}

.card{
background:white;
padding:12px;
border-radius:10px;
border:1px solid #e0e0e0;
text-align:center;
margin-bottom:10px;
}

.badge{
padding:5px 10px;
border-radius:20px;
color:white;
font-size:13px;
}

.green{background:#2ecc71;}
.orange{background:#f39c12;}
.red{background:#e74c3c;}

.volume-box{
background:#e8f8f5;
padding:20px;
border-radius:12px;
font-size:36px;
font-weight:700;
text-align:center;
}

div.stButton > button{
background:#1f77ff;
color:white;
border-radius:6px;
height:36px;
}

</style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------
h_left, h_right = st.columns([6,2])

with h_left:
    st.markdown('<div class="header">Gesture Based Volume Control System</div>', unsafe_allow_html=True)

with h_right:
    b1,b2,b3 = st.columns(3)
    start_btn = b1.button("Start")
    stop_btn = b2.button("Stop")
    capture_btn = b3.button("Capture")

# -------------------- LAYOUT --------------------
left_col, right_col = st.columns([4,1.5])

camera_placeholder = left_col.empty()
graph1_placeholder = left_col.empty()
graph2_placeholder = left_col.empty()

with right_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    st.subheader("Detection Status")
    cam_status = st.empty()
    fps_status = st.empty()
    hands_status = st.empty()

    st.markdown("---")

    st.subheader("Gesture Info")
    distance_card = st.empty()
    gesture_card = st.empty()
    distance_bar = st.progress(0)

    st.markdown("---")

    st.subheader("Volume Control")
    volume_display = st.empty()

    st.markdown("---")

    st.subheader("Performance Metrics")
    response_metric = st.empty()
    accuracy_metric = st.empty()

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------- MEDIAPIPE --------------------
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75,
    max_num_hands=2
)

# -------------------- VOLUME CONTROL --------------------
system_os = platform.system()

if system_os == "Windows":
    import comtypes
    comtypes.CoInitialize()

    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    def set_volume(v):
        volume.SetMasterVolumeLevelScalar(v/100,None)

    def get_volume():
        return int(volume.GetMasterVolumeLevelScalar()*100)

else:
    def set_volume(v):
        pass
    def get_volume():
        return 50

# -------------------- SESSION STATE --------------------
if "run" not in st.session_state:
    st.session_state.run = False

if start_btn:
    st.session_state.run = True

if stop_btn:
    st.session_state.run = False

# -------------------- DATA STORAGE --------------------
volume_history = deque(maxlen=40)

smooth_volume = 0

total_frames = 0
detected_frames = 0
PIXEL_TO_MM = 0.26

# -------------------- GESTURE CLASSIFIER --------------------
def classify_gesture(distance):

    if distance < 30:
        return "Closed","red"
    elif distance < 80:
        return "Pinch","orange"
    else:
        return "Open Hand","green"

# -------------------- CAMERA LOOP --------------------
if st.session_state.run:

    cap = cv2.VideoCapture(0)
    prev_time = time.time()

    while st.session_state.run:

        start_time = time.time()

        ret, frame = cap.read()
        if not ret:
            st.error("Camera not detected")
            break

        total_frames += 1

        frame = cv2.flip(frame,1)
        h,w,_ = frame.shape

        rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        distance = 0
        gesture = "None"
        color = "green"
        hand_count = 0
        volume_val = get_volume()

        if results.multi_hand_landmarks:

            detected_frames += 1
            hand_count = len(results.multi_hand_landmarks)

            for hand in results.multi_hand_landmarks:

                thumb = hand.landmark[4]
                index = hand.landmark[8]

                x1,y1 = int(thumb.x*w), int(thumb.y*h)
                x2,y2 = int(index.x*w), int(index.y*h)

                distance_px = math.hypot(x2-x1,y2-y1)
                distance = distance_px * PIXEL_TO_MM

                gesture,color = classify_gesture(distance)

                vol = np.interp(distance,[20,120],[0,100])

                smooth_volume = int(0.8*smooth_volume + 0.2*vol)

                set_volume(smooth_volume)
                volume_val = smooth_volume

                cv2.circle(frame,(x1,y1),8,(255,0,255),-1)
                cv2.circle(frame,(x2,y2),8,(255,0,255),-1)
                cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),3)

                mp_draw.draw_landmarks(frame,hand,mp_hands.HAND_CONNECTIONS)

        # -------------------- FPS --------------------
        curr_time = time.time()
        fps = int(1/(curr_time-prev_time))
        prev_time = curr_time

        # -------------------- RESPONSE TIME --------------------
        response_time = int((time.time() - start_time)*1000)

        # -------------------- ACCURACY --------------------
        if total_frames > 0:
            accuracy = (detected_frames/total_frames)*100
        else:
            accuracy = 0

        # -------------------- UI UPDATE --------------------

        camera_placeholder.image(frame,channels="BGR")

        cam_status.markdown(f"Camera: **Active**")
        fps_status.markdown(f"FPS: **{fps}**")
        hands_status.markdown(f"Hands Detected: **{hand_count}**")

        distance_card.markdown(f"""
        <div class="card">
        <h2>{distance:.2f}</h2>
        Distance (mm)
        </div>
        """,unsafe_allow_html=True)

        gesture_card.markdown(f"""
        <div class="card">
        Gesture : <span class="badge {color}">{gesture}</span>
        </div>
        """,unsafe_allow_html=True)

        distance_bar.progress(min(distance/40,1.0))

        volume_display.markdown(
            f'<div class="volume-box">{volume_val}%</div>',
            unsafe_allow_html=True
        )

        response_metric.markdown(f"Response Time : **{response_time} ms**")
        accuracy_metric.markdown(f"Detection Accuracy : **{accuracy:.2f}%**")

        volume_history.append(volume_val)

        # -------------------- GRAPH 1 --------------------
        fig,ax = plt.subplots()

        ax.set_xlim(0,120)
        ax.set_ylim(0,100)
        ax.set_xlabel("Distance")
        ax.set_ylabel("Volume")

        ax.plot([0,120],[0,100])
        ax.scatter(distance,volume_val)

        ax.set_title("Distance → Volume Mapping")

        graph1_placeholder.pyplot(fig)
        plt.close()

        # -------------------- GRAPH 2 --------------------
        fig2,ax2 = plt.subplots()

        ax2.plot(list(volume_history))
        ax2.set_ylim(0,100)
        ax2.set_title("Volume History")

        graph2_placeholder.pyplot(fig2)
        plt.close()

        if capture_btn:
            cv2.imwrite("captured_frame.png",frame)
            st.toast("Frame Captured")

        time.sleep(0.03)

    cap.release()

else:
    st.info("Click Start to activate the system")

