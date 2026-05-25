# main.py — Phase 6: Touchless Desktop Interaction System
#
# Full pipeline:
#   ThreadedCapture
#     → process_frame (grayscale, thermal, edges)
#     → pixels_to_ascii
#     → HandTracker.process
#     → GestureStateMachine.update  (gesture stabilisation)
#     → InteractionModeManager.update  (mode logic + cursor + actions)
#     → render ASCII + draw layer + skeleton + cursor + HUD

import time
import signal
import sys

from processor    import process_frame
from ascii_mapper import pixels_to_ascii
from renderer     import (
    init_window, render_thermal, render_edge,
    render_draw_layer, render_cursor,
    draw_hud, poll_keys, close_window, _canvas
)
from config import TARGET_FPS, RENDER_MODE, USE_THREADED_CAPTURE, ENABLE_HAND_TRACKING


def build_camera():
    if USE_THREADED_CAPTURE:
        from threaded_capture import ThreadedCapture
        return ThreadedCapture()
    from capture import WebcamCapture
    return WebcamCapture()


def main():
    camera         = build_camera()
    frame_interval = 1.0 / TARGET_FPS
    current_mode   = RENDER_MODE

    # ── Optional modules ─────────────────────────────────────────────────────
    tracker    = None
    gsm        = None
    mode_mgr   = None
    draw_layer = None

    if ENABLE_HAND_TRACKING:
        from hand_tracker      import HandTracker
        from gesture_state     import GestureStateMachine
        from gesture_actions   import CursorController, ActionController
        from interaction_mode  import InteractionModeManager
        from draw_layer        import DrawLayer

        tracker    = HandTracker()
        gsm        = GestureStateMachine()
        draw_layer = DrawLayer()
        cursor_ctl = CursorController()
        action_ctl = ActionController()
        mode_mgr   = InteractionModeManager(cursor_ctl, action_ctl, draw_layer)

        print("Hand tracking    : ENABLED")
        print("Interaction modes: ENABLED  (navigate / select / drag / draw / scroll)")
        print("Draw layer       : ENABLED  (pinch to draw, C to clear)")
    else:
        print("Hand tracking    : DISABLED")

    # ── Clean exit ────────────────────────────────────────────────────────────
    def on_exit(sig=None, _frame=None):
        if mode_mgr:
            mode_mgr.reset()
        if tracker:
            tracker.release()
        close_window()
        camera.release()
        print("\nExited cleanly.")
        sys.exit(0)

    signal.signal(signal.SIGINT, on_exit)

    print(f"\nRender mode : {current_mode}  |  Target FPS : {TARGET_FPS}")
    print("Keys        : [E] edge  [T] tracking  [C] clear drawing  [Q] quit")
    time.sleep(1.5)
    init_window()

    # ── Runtime state ─────────────────────────────────────────────────────────
    tracking_active = ENABLE_HAND_TRACKING
    frame_count     = 0
    fps_display     = 0.0
    fps_timer       = time.time()
    last_action     = ""
    hand_results    = []
    tip_canvas      = None    # smoothed fingertip for cursor rendering

    # ── Main loop ─────────────────────────────────────────────────────────────
    while True:
        loop_start = time.perf_counter()

        # Stage 1 — Capture
        frame = camera.read_frame()
        if frame is None:
            print("\nCamera stalled. Exiting.")
            on_exit()

        # Stage 2 — Process
        gray_resized, color_resized, edge_mask = process_frame(frame)

        # Stage 3 — ASCII
        ascii_rows = pixels_to_ascii(gray_resized)

        # Stage 4 — Hand tracking
        hand_results = []
        tip_canvas   = None
        if tracker and tracking_active:
            hand_results = tracker.process(frame)
            hand_present = len(hand_results) > 0

            raw_gesture = hand_results[0].gesture if hand_present else 'none'

            # Gesture stabilisation
            gsm.update(raw_gesture, hand_present)

            # Mode manager drives cursor + actions
            if hand_present:
                tip_canvas = hand_results[0].index_tip_canvas
                result = mode_mgr.update(gsm.stable_gesture, tip_canvas, True)
            else:
                result = mode_mgr.update('none', (0, 0), False)

            if result:
                last_action = result
        else:
            if gsm:
                gsm.reset()
            if mode_mgr:
                mode_mgr.reset()

        # Stage 5 — FPS
        frame_count += 1
        elapsed = time.time() - fps_timer
        if elapsed >= 1.0:
            fps_display = frame_count / elapsed
            frame_count = 0
            fps_timer   = time.time()

        # Stage 6 — Render ASCII base
        if current_mode == 'thermal':
            render_thermal(ascii_rows, color_resized)
        else:
            render_edge(ascii_rows, color_resized, edge_mask)

        # Stage 7 — Draw layer (strokes on top of ASCII)
        if draw_layer:
            render_draw_layer(draw_layer)

        # Stage 8 — Hand skeleton overlay
        if tracker and tracking_active and hand_results:
            tracker.draw_skeleton(_canvas, hand_results)

        # Stage 9 — Mode-colored cursor
        if tip_canvas and mode_mgr:
            render_cursor(tip_canvas, mode_mgr.mode_name, gsm_locked=gsm.locked if gsm else False)

        # Stage 10 — HUD
        draw_hud(
            fps             = fps_display,
            render_mode     = current_mode,
            gsm             = gsm if tracking_active else None,
            mode_mgr        = mode_mgr if tracking_active else None,
            last_action     = last_action,
            tracking_active = tracking_active,
            draw_layer      = draw_layer,
        )

        # Stage 11 — Keys
        key = poll_keys()
        if key == 'q':
            on_exit()
        elif key == 'e':
            current_mode = 'edge' if current_mode == 'thermal' else 'thermal'
        elif key == 't':
            tracking_active = not tracking_active
            if not tracking_active and mode_mgr:
                mode_mgr.reset()
            last_action = ''
        elif key == 'c':
            if draw_layer:
                draw_layer.clear()
                last_action = 'CANVAS CLEARED'

        # Stage 12 — Frame cap
        sleep_t = frame_interval - (time.perf_counter() - loop_start)
        if sleep_t > 0:
            time.sleep(sleep_t)


if __name__ == "__main__":
    main()
