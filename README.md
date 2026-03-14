# 🎛 Gesture Based Volume Control Dashboard

## 📌 Project Overview
The **Gesture Based Volume Control Dashboard** is a real-time computer vision system that allows users to control their system volume using hand gestures detected through a webcam.

The system tracks hand landmarks using **MediaPipe**, calculates the distance between the **thumb and index finger**, and maps this distance to system volume levels. The application also provides a **visual analytics dashboard** displaying gesture information, detection performance, and real-time graphs.

The dashboard is built using **Streamlit**, making it interactive and easy to use while providing visual insights into the gesture detection process.

---

# 🎯 Objectives
- Detect hand gestures in real time using a webcam
- Measure distance between thumb and index finger
- Map finger distance to system volume level
- Control device volume using gestures
- Display gesture detection metrics and performance statistics
- Visualize volume control behavior using graphs

---

# 🛠 Technologies Used

| Technology | Purpose |
|------------|--------|
| Python | Core programming language |
| Streamlit | Web-based dashboard interface |
| OpenCV | Webcam capture and image processing |
| MediaPipe | Hand landmark detection |
| NumPy | Mathematical computations |
| Matplotlib | Graph visualization |
| Pycaw | Windows system volume control |
| Collections (deque) | Volume history tracking |

---

# 📂 Project Structure

```
HAND_GESTURE_MILESTONE4
│
├── main.py
├── README.md
└── captured_frame.png
```

---

# ⚙ Installation

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/akhilakummari-26/HAND_GESTURE_MILESTONE_4.git

```

---

## 2️⃣ Install Dependencies

```bash
 Install the below libraries

```bash
pip install streamlit opencv-python mediapipe numpy matplotlib pycaw comtypes
```

---

# ▶ Running the Application

Run the Streamlit application using:

```bash
streamlit run main.py
```

Then open in browser:

```
http://localhost:8501
```

---

# 🖥 System Interface

The application dashboard is divided into **two main sections**.

---

# 🎥 Left Panel

### Live Camera Feed
Displays the real-time webcam video with:
- Hand landmark detection
- Finger distance visualization
- Gesture recognition overlay

### Distance → Volume Mapping Graph
Shows the relationship between:
- Finger distance
- System volume level

### Volume History Graph
Displays how volume changes over time during gesture control.

---

# 📊 Right Panel

### Detection Status
Shows system status including:
- Camera activity
- Frames per second (FPS)
- Number of hands detected

### Gesture Information
Displays:
- Measured finger distance
- Current gesture classification
- Distance progress bar

### Volume Control
Displays the current **system volume percentage**.

### Performance Metrics
Shows system performance statistics:
- Response time
- Detection accuracy

---

# ✋ Gesture Recognition Logic

The system detects two key hand landmarks:

- **Thumb Tip → Landmark 4**
- **Index Finger Tip → Landmark 8**

Distance between these landmarks is calculated using:

```
distance = √((x2 - x1)² + (y2 - y1)²)
```

The pixel distance is converted to millimeters using:

```
distance_mm = pixel_distance × 0.26
```

---

# 🤚 Gesture Classification

| Gesture | Distance Range |
|-------|----------------|
| Closed | < 30 mm |
| Pinch | 30 – 80 mm |
| Open Hand | > 80 mm |

---

# 🔊 Volume Mapping

Finger distance is mapped to volume using interpolation:

```
Volume = interpolate(distance,[20,120] → [0,100])
```

Where:
- **20 mm → 0% volume**
- **120 mm → 100% volume**

This creates smooth gesture-based volume control.

---

# 📈 Features

- Real-time hand gesture detection
- Gesture-based volume control
- Smooth volume interpolation
- Distance-to-volume visualization
- Volume history tracking
- Performance metrics display
- Interactive Streamlit dashboard

---

# 💻 Supported Platforms

| OS | Volume Control |
|----|----------------|
| Windows | Pycaw API |
| macOS | Can be extended with AppleScript |
| Linux | Can be extended with amixer |

---

# 📊 Performance Metrics

The system tracks:

- **Detection FPS**
- **Response Time (ms)**
- **Detection Accuracy (%)**

These metrics help evaluate the efficiency of the gesture recognition pipeline.

---

# 🚀 Future Improvements

Potential future enhancements:

- Multi-gesture support
- AI-based gesture classification
- Media playback gesture controls
- Smart home device integration
- Mobile camera integration
- Deep learning gesture recognition

---

# 📚 Applications

Gesture-based interaction systems can be used in:

- Touchless computer interfaces
- Smart home control systems
- Assistive technologies
- Medical environments
- Gaming and AR/VR systems
- Interactive public displays

---

# 👩‍💻 Author

**Akhila Kummari**

---

# 📜 License

This project is licensed under the MIT License.
