import cv2
import os
from utils.config_loader import load_config
from features import recorder, filters, overlay, screenshot

def open_source(source):
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print(f"Failed to open source: {source}")
        return None
    return cap

def main():
    config = load_config()
    target_w = int(config["frame_width"])
    target_h = int(config["frame_height"])
    os.makedirs(config["output_dir"], exist_ok=True)

    sources = config.get("sources", [0])
    current_source_idx = 0
    cap = open_source(sources[current_source_idx])
    if cap is None:
        return
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, target_w)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, target_h)

    out = None
    recording = False
    filter_mode = "normal"

    print("▶ RecLite started")
    print("SPACE=Record/Stop | S=Screenshot | 1/2/3=Filters | TAB=Switch Source | ESC=Exit")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Frame grab failed, retrying...")
            continue

        frame = filters.apply_filter(frame, mode=filter_mode,
                                     alpha=config["contrast"], beta=config["brightness"])

        if recording and out:
            overlay.draw_record_indicator(frame)
            if frame.shape[1] != target_w or frame.shape[0] != target_h:
                frame_to_write = cv2.resize(frame, (target_w, target_h))
            else:
                frame_to_write = frame
            if frame_to_write.ndim == 2:
                frame_to_write = cv2.cvtColor(frame_to_write, cv2.COLOR_GRAY2BGR)
            out.write(frame_to_write)

        overlay.draw_info(frame, config["fps"])
        overlay.draw_help(frame, recording, filter_mode, current_source_idx, len(sources))
        cv2.imshow("RecLite", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == 32:
            recording = not recording
            if recording:
                try:
                    out, fname = recorder.init_writer(config)
                    print(f"Recording started: {fname}")
                except Exception as e:
                    print(f"Recording failed: {e}")
                    recording = False
                    out = None
            else:
                if out: out.release()
                out = None
                print("Recording stopped")

        elif key == ord("s"):
            screenshot.save_screenshot(frame, config["output_dir"])

        elif key == ord("1"):
            filter_mode = "normal"
        elif key == ord("2"):
            filter_mode = "gray"
        elif key == ord("3"):
            filter_mode = "canny"
        elif key == ord("4"):
            filter_mode = "sepia"
        elif key == ord("5"):
            filter_mode = "flip_h"
        elif key == ord("6"):
            filter_mode = "flip_v"

        elif key == 9:
            current_source_idx = (current_source_idx + 1) % len(sources)
            print(f"🔄 Switching source → {sources[current_source_idx]}")
            cap.release()
            cap = open_source(sources[current_source_idx])
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, target_w)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, target_h)

        elif key == 27:
            print("Exit program")
            break

    cap.release()
    if out: out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()