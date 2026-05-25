# renderer.py — Phase 6: fullscreen, mode-colored cursor, draw overlay, rich HUD.

import sys
import numpy as np
import cv2
from config import (
    CELL_W, CELL_H, ASCII_WIDTH, ASCII_HEIGHT,
    FONT, FONT_SCALE, FONT_THICKNESS, WINDOW_NAME,
    EDGE_COLOR, EDGE_ALPHA, MODE_CURSOR_COLORS,
)

# ── Terminal renderer (Phase 1 compat) ───────────────────────────────────────
def clear_and_render(ascii_rows):
    sys.stdout.write('\033[H' + '\n'.join(ascii_rows))
    sys.stdout.flush()

def hide_cursor():
    sys.stdout.write('\033[?25l'); sys.stdout.flush()

def show_cursor():
    sys.stdout.write('\033[?25h'); sys.stdout.flush()


# ── Canvas ────────────────────────────────────────────────────────────────────
_CANVAS_H = ASCII_HEIGHT * CELL_H
_CANVAS_W = ASCII_WIDTH  * CELL_W
_canvas   = np.zeros((_CANVAS_H, _CANVAS_W, 3), dtype=np.uint8)

_col_xs = np.arange(ASCII_WIDTH)  * CELL_W
_row_ys = (np.arange(ASCII_HEIGHT) + 1) * CELL_H


def init_window():
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN,
                          cv2.WINDOW_FULLSCREEN)


# ── ASCII renderers ───────────────────────────────────────────────────────────
def render_thermal(ascii_rows, color_grid):
    _canvas.fill(0)
    for row_idx, row_str in enumerate(ascii_rows):
        y = int(_row_ys[row_idx])
        for col_idx, char in enumerate(row_str):
            if char == ' ':
                continue
            bgr = color_grid[row_idx, col_idx]
            cv2.putText(_canvas, char, (int(_col_xs[col_idx]), y),
                        FONT, FONT_SCALE,
                        (int(bgr[0]), int(bgr[1]), int(bgr[2])),
                        FONT_THICKNESS, cv2.LINE_AA)


def render_edge(ascii_rows, color_grid, edge_mask):
    _canvas.fill(0)
    ec = np.array(EDGE_COLOR, dtype=np.float32)
    for row_idx, row_str in enumerate(ascii_rows):
        y = int(_row_ys[row_idx])
        for col_idx, char in enumerate(row_str):
            if char == ' ':
                continue
            bgr = color_grid[row_idx, col_idx]
            if edge_mask[row_idx, col_idx] > 0:
                tc    = np.array([bgr[0], bgr[1], bgr[2]], dtype=np.float32)
                mixed = ec * EDGE_ALPHA + tc * (1.0 - EDGE_ALPHA)
                color = (int(mixed[0]), int(mixed[1]), int(mixed[2]))
            else:
                color = (int(bgr[0]), int(bgr[1]), int(bgr[2]))
            cv2.putText(_canvas, char, (int(_col_xs[col_idx]), y),
                        FONT, FONT_SCALE, color, FONT_THICKNESS, cv2.LINE_AA)


# ── Draw layer overlay ────────────────────────────────────────────────────────
def render_draw_layer(draw_layer):
    """Render stroke overlay on top of the ASCII canvas."""
    draw_layer.render(_canvas)


# ── Mode-colored cursor ───────────────────────────────────────────────────────
def render_cursor(tip_xy, mode_name, gsm_locked=False):
    """
    Draw the interaction cursor at the index fingertip position.
    Ring color = current mode. Inner dot = white.
    Pulses (double ring) when a gesture is locked in.
    """
    if tip_xy is None:
        return
    x, y = tip_xy
    color = MODE_CURSOR_COLORS.get(mode_name, (200, 200, 200))
    cv2.circle(_canvas, (x, y), 10, color, 2, cv2.LINE_AA)
    cv2.circle(_canvas, (x, y), 3,  color, -1, cv2.LINE_AA)
    if gsm_locked:
        cv2.circle(_canvas, (x, y), 15, color, 1, cv2.LINE_AA)


# ── HUD ───────────────────────────────────────────────────────────────────────
_MODE_ICONS = {
    'navigate': '>',
    'select':   'V',
    'drag':     '[X]',
    'draw':     'D',
    'scroll':   '=',
}

_MODE_LABEL_COLORS = {
    'navigate': (0,   220, 160),
    'select':   (200, 100, 255),
    'drag':     (0,   180, 255),
    'draw':     (80,  80,  255),
    'scroll':   (255, 180,  50),
}


def draw_hud(fps, render_mode, gsm=None, mode_mgr=None,
             last_action='', tracking_active=True, draw_layer=None):
    """
    Full HUD overlay:
      Top bar       — FPS, render mode, key hints
      Mode panel    — current interaction mode + dwell bar
      Gesture panel — current stable gesture + state machine state
      Bottom bar    — last action + draw stroke count
    """
    h, w = _canvas.shape[:2]
    TOP  = 18

    # ── Top bar ───────────────────────────────────────────────────────────────
    cv2.rectangle(_canvas, (0, 0), (w, TOP), (18, 18, 18), -1)
    fps_str = (f" FPS:{fps:4.1f}  [{render_mode.upper()}]"
               f"  [E]edge [T]track [C]clear [Q]quit"
               f"{'  TRACKING OFF' if not tracking_active else ''}")
    cv2.putText(_canvas, fps_str, (4, 13),
                FONT, 0.33, (170, 170, 170), 1, cv2.LINE_AA)

    if not tracking_active or mode_mgr is None:
        _show()
        return

    # ── Mode panel (left) ─────────────────────────────────────────────────────
    mode_name  = mode_mgr.mode_name
    mode_color = _MODE_LABEL_COLORS.get(mode_name, (160, 160, 160))
    mode_icon  = _MODE_ICONS.get(mode_name, '?')

    px, py, pw, ph = 6, TOP + 4, 138, 84
    _translucent_rect(px, py, px + pw, py + ph, alpha=0.68)

    cv2.putText(_canvas, 'MODE', (px + 4, py + 14),
                FONT, 0.30, (100, 100, 100), 1, cv2.LINE_AA)
    cv2.putText(_canvas, f"{mode_icon}  {mode_name.upper()}",
                (px + 4, py + 34),
                FONT, 0.52, mode_color, 1, cv2.LINE_AA)

    # Dwell / mode-switch progress bar
    _progress_bar(_canvas,
                  x0=px + 4, y0=py + 46, width=pw - 8, height=7,
                  progress=mode_mgr.dwell_progress,
                  color=mode_color, bg=(40, 40, 40))
    cv2.putText(_canvas, f"switch {mode_mgr.dwell_progress*100:3.0f}%",
                (px + 4, py + 65),
                FONT, 0.27, (90, 90, 90), 1, cv2.LINE_AA)

    # Draw stroke count (shown when in draw mode)
    if mode_name == 'draw' and draw_layer is not None:
        cv2.putText(_canvas, f"strokes: {draw_layer.stroke_count()}",
                    (px + 4, py + 78),
                    FONT, 0.27, mode_color, 1, cv2.LINE_AA)

    # ── Gesture panel (left, below mode panel) ────────────────────────────────
    if gsm is not None:
        gx, gy, gw, gh = 6, TOP + ph + 10, 138, 72
        _translucent_rect(gx, gy, gx + gw, gy + gh, alpha=0.65)

        gesture = gsm.stable_gesture
        g_color = _gesture_color(gesture)

        cv2.putText(_canvas, gsm.state.name, (gx + 4, gy + 14),
                    FONT, 0.28, (90, 90, 90), 1, cv2.LINE_AA)
        cv2.putText(_canvas, gesture, (gx + 4, gy + 34),
                    FONT, 0.50, g_color, 1, cv2.LINE_AA)

        _progress_bar(_canvas,
                      x0=gx + 4, y0=gy + 44, width=gw - 8, height=6,
                      progress=gsm.dwell_progress,
                      color=(0, 255, 120) if not gsm.locked else (0, 200, 255),
                      bg=(40, 40, 40))
        cv2.putText(_canvas, f"dwell {gsm.dwell_progress*100:3.0f}%",
                    (gx + 4, gy + 62),
                    FONT, 0.27, (90, 90, 90), 1, cv2.LINE_AA)

    # ── Bottom bar — last action ───────────────────────────────────────────────
    if last_action:
        cv2.rectangle(_canvas, (0, h - 20), (w, h), (18, 18, 18), -1)
        a_color = (0, 255, 180) if '[demo]' not in last_action else (160, 160, 0)
        cv2.putText(_canvas, f" {last_action}", (4, h - 6),
                    FONT, 0.40, a_color, 1, cv2.LINE_AA)

    _show()


# ── Helpers ───────────────────────────────────────────────────────────────────
def _translucent_rect(x0, y0, x1, y1, alpha=0.7, color=(14, 14, 14)):
    overlay = _canvas.copy()
    cv2.rectangle(overlay, (x0, y0), (x1, y1), color, -1)
    cv2.addWeighted(overlay, alpha, _canvas, 1 - alpha, 0, _canvas)


def _progress_bar(canvas, x0, y0, width, height, progress, color, bg):
    cv2.rectangle(canvas, (x0, y0), (x0 + width, y0 + height), bg, -1)
    fill = int(width * max(0.0, min(progress, 1.0)))
    if fill > 0:
        cv2.rectangle(canvas, (x0, y0), (x0 + fill, y0 + height), color, -1)


_GESTURE_COLORS_HUD = {
    'point': (0,   220, 255),
    'peace': (80,  255, 80),
    'fist':  (80,  80,  255),
    'open':  (255, 200, 0),
    'pinch': (200, 80,  255),
    'none':  (100, 100, 100),
}

def _gesture_color(gesture):
    return _GESTURE_COLORS_HUD.get(gesture, (140, 140, 140))


def _show():
    cv2.imshow(WINDOW_NAME, _canvas)


def poll_keys():
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'): return 'q'
    if key == ord('e'): return 'e'
    if key == ord('t'): return 't'
    if key == ord('c'): return 'c'
    return True


def close_window():
    cv2.destroyAllWindows()
