# config.py — all tunable constants for all phases.

import cv2

# ── Camera ───────────────────────────────────────────────────────────────────
CAMERA_INDEX    = 0
FLIP_HORIZONTAL = True

# ── ASCII grid ────────────────────────────────────────────────────────────────
ASCII_WIDTH  = 120
ASCII_HEIGHT = 45
ASCII_CHARS  = " .`'^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhaeo*#MW&8%B@$"

# ── Frame rate ────────────────────────────────────────────────────────────────
TARGET_FPS = 30

# ── Render mode ───────────────────────────────────────────────────────────────
RENDER_MODE = 'thermal'

# ── Colormap ──────────────────────────────────────────────────────────────────
COLORMAP = cv2.COLORMAP_INFERNO

# ── Edge detection ────────────────────────────────────────────────────────────
CANNY_LOW  = 50
CANNY_HIGH = 150
EDGE_COLOR = (0, 255, 255)
EDGE_ALPHA = 0.85

# ── Font / window ─────────────────────────────────────────────────────────────
FONT           = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE     = 0.4
FONT_THICKNESS = 1
CELL_W         = 7
CELL_H         = 13
WINDOW_NAME    = "Gesture OS — Phase 6"

# ── Performance ───────────────────────────────────────────────────────────────
USE_THREADED_CAPTURE = True

# ── Hand tracking ─────────────────────────────────────────────────────────────
HAND_DETECTION_CONFIDENCE = 0.7
HAND_TRACKING_CONFIDENCE  = 0.6
MAX_HANDS                 = 1
ENABLE_HAND_TRACKING      = True

# ── One Euro Filter ───────────────────────────────────────────────────────────
OEF_FREQ   = 30.0
OEF_FC_MIN = 1.0
OEF_BETA   = 0.01

# ── Gesture state machine ─────────────────────────────────────────────────────
GESTURE_BUFFER_SIZE       = 7
GESTURE_DWELL_FRAMES      = 8
GESTURE_HYSTERESIS_FRAMES = 4
GESTURE_COOLDOWN_SEC      = 0.8

# ── PC control ───────────────────────────────────────────────────────────────
ENABLE_PC_CONTROL    = False
CURSOR_DEAD_ZONE     = 0.04
CURSOR_MODE          = 'relative'
CURSOR_RELATIVE_SPEED = 2.5
CURSOR_EDGE_CLIP     = 0.08

# ── Phase 6: Interaction modes ────────────────────────────────────────────────
# Gesture that enters each mode from Navigation.
# Keep this as a lookup table — easy to remap without touching logic.
MODE_ENTRY_GESTURES = {
    'navigate': 'point',     # default, always active when pointing
    'select':   'peace',     # index+middle up → click/confirm actions
    'drag':     'fist',      # all fingers curled → drag lock
    'draw':     'pinch',     # thumb+index touch → draw strokes
    'scroll':   'open',      # all fingers spread → scroll/pan
}

# Frames a mode-entry gesture must be held before mode switches.
# Higher = less accidental mode changes, more deliberate feel.
MODE_DWELL_FRAMES = 10

# Seconds to ignore mode-switch attempts after a switch fires.
# Prevents instant re-entering of previous mode.
MODE_SWITCH_COOLDOWN = 1.2

# Cursor color per mode (BGR). Shown as cursor ring color in the window.
MODE_CURSOR_COLORS = {
    'navigate': (0,   220, 160),   # teal-green
    'select':   (200, 100, 255),   # purple
    'drag':     (0,   180, 255),   # amber
    'draw':     (80,  80,  255),   # coral-red
    'scroll':   (255, 180, 50),    # blue
}

# ── Phase 6: Draw layer ───────────────────────────────────────────────────────
# Maximum number of polyline strokes kept in memory.
# Older strokes are dropped when limit is exceeded.
DRAW_MAX_STROKES = 50

# Minimum distance (canvas pixels) between successive draw points.
# Prevents storing thousands of nearly-identical points on slow hand moves.
DRAW_MIN_POINT_DIST = 3

# Stroke line thickness on the canvas (pixels).
DRAW_STROKE_THICKNESS = 2

# Stroke color in draw mode (BGR). Set None to use mode cursor color.
DRAW_STROKE_COLOR = None   # None = use MODE_CURSOR_COLORS['draw']

# Fade strokes over time? Set 0 to keep strokes forever.
# Set e.g. 8.0 to fade strokes out after 8 seconds.
DRAW_STROKE_FADE_SEC = 0.0

# ── Phase 6: Scroll mode ─────────────────────────────────────────────────────
# How many pyautogui scroll units per canvas-pixel of vertical hand movement.
SCROLL_SENSITIVITY = 0.15
