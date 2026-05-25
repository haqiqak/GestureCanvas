# GestureCanvas
A gesture-controlled virtual interaction system for touchless drawing, teaching, and spatial UI experimentation using computer vision.

# Touchless Thermal ASCII Interface
This project began as an experimental ASCII thermal renderer and is evolving into a broader gesture-driven interaction environment including touchless drawing boards, interactive teaching interfaces, accessibility-focused controls, and desktop interaction systems.

The project combines:
- computer vision
- gesture recognition
- real-time rendering
- interaction design

It is now evolving toward a broader touchless interaction ecosystem focused on drawing, accessibility, education, and gesture-based computing.

---

# What It Currently Does

The current system can:

- Capture live webcam video
- Convert frames into thermal-style ASCII art
- Detect and track hands in real time
- Recognize basic hand gestures
- Display gesture-aware overlays and HUD elements
- Smooth cursor movement for more natural interaction
- Support fullscreen interaction rendering
- Maintain gesture stability using dwell and cooldown systems

Current gestures implemented:
- `point`
- `peace`
- `fist`
- `open`
- `pinch`

The architecture is modular, allowing interaction systems to evolve independently from rendering systems.

---

# Core Technologies

- Python
- OpenCV
- MediaPipe
- NumPy

---

# Current System Pipeline

```text
Webcam Feed
    ↓
Frame Processing
    ↓
Thermal ASCII Conversion
    ↓
Hand Landmark Detection
    ↓
Gesture Recognition
    ↓
Cursor / Interaction Logic
    ↓
HUD + Overlay Rendering
```

---

# Current Project Structure

```text
cam/
├── main.py
├── hand_tracker.py
├── gesture_actions.py
├── gesture_state.py
├── one_euro_filter.py
├── renderer.py
├── processor.py
├── ascii_mapper.py
├── capture.py
├── threaded_capture.py
├── config.py
├── requirements.txt
└── hand_landmarker.task
```

---

# Features Currently Implemented

## Thermal ASCII Rendering
The webcam feed is transformed into a thermal-inspired ASCII visualization using brightness mapping and colored rendering.

## Real-Time Hand Tracking
Hands are tracked using MediaPipe landmark detection.

## Gesture Recognition
Basic gestures are classified using rule-based logic built on landmark positions.

## Gesture State Logic
The system includes:
- gesture buffering
- dwell timing
- cooldown management
- hysteresis stabilization

This improves interaction quality and reduces accidental triggers.

## Adaptive Cursor Smoothing
A One Euro Filter is used to reduce jitter while preserving responsiveness during fast motion.

## Fullscreen Interaction HUD
The renderer displays:
- gesture state
- tracking status
- dwell progression
- interaction overlays

---

# Vision For The Project

The long-term goal is to evolve this into a configurable touchless interaction platform.

The project is intended to grow beyond a demo into a practical gesture-based operating environment where users can interact with applications and digital spaces entirely through hand movement.

---

# Planned Directions

## Touchless Drawing Board
One major direction is turning the system into a gesture-driven drawing and teaching environment.

Planned capabilities:
- air drawing
- gesture-based brush selection
- color selection through gestures
- erasing using gestures
- whiteboard mode
- presentation mode
- annotation tools
- teaching interface support

The idea is to allow users to teach, explain, sketch, and interact with a digital board entirely without physical contact.

---

## Gesture-Based Desktop Interaction

Future versions may support:
- cursor navigation
- scrolling
- media control
- app switching
- volume adjustment
- brightness adjustment
- configurable gesture shortcuts

The long-term vision is a customizable touchless desktop interaction system.

---

## Accessibility & Inclusive Interaction

Another major ambition is accessibility.

The project is being explored as a possible foundation for:
- hands-free interaction systems
- mobility-friendly interfaces
- touchless educational tools
- distance-based interaction environments

The goal is not only experimental interaction design, but also exploring how gesture systems can make computing more accessible.

---

# Planned Features

- Multi-hand interaction
- Air-writing support
- Gesture-configurable commands
- User-defined gesture mappings
- Drawing layers
- Save/export drawings
- Gesture macros
- Collaborative interaction modes
- Touchless UI widgets
- Interactive teaching boards
- Presentation controls
- Gesture calibration profiles

---

# Installation

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# MediaPipe Model File

This project uses the newer MediaPipe Tasks API and requires:

```text
hand_landmarker.task
```

Place the file in the root project directory.

---

# Run The Project

```bash
python main.py
```

---

# Controls

| Key | Action |
|------|--------|
| Q | Quit |
| E | Toggle edge mode |
| T | Toggle tracking |

---

# Current Development Status

This project is experimental and actively evolving.

Current focus areas:
- interaction quality
- gesture stability
- cursor semantics
- rendering performance
- modular architecture
- touchless interaction design

---

# Research Areas Behind The Project

The project also acts as a learning and experimentation platform for:
- Human-Computer Interaction (HCI)
- Computer Vision
- Gesture Semantics
- Spatial Interfaces
- Accessibility Systems
- Real-Time Interactive Systems
- Touchless Educational Interfaces

---

Haqiq Azeem.
