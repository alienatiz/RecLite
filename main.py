import cv2
import os
from utils.config_loader import load_config
from features import recorder, filters, overlay, screenshot

def main():
    config = load_config()
    os.makedirs(config["output_dir"], exist_ok=True)

    cap = cv2.VideoCapture(config["camera_index"])
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config["frame_width"])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config["frame_height"])

    out = None
    recording = False
    filter_mode = "normal"

    print("▶ RecLite started")
    print("SPACE=Record/Stop | S=Screenshot | 1/2/3=Filters | ESC=Exit")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = filters.apply_filter(
            frame, mode=filter_mode,
            alpha=config["contrast"], beta=config["brightness"]
        )
        help_texts = [
            "SPACE = Record/Stop",
            "S = Screenshot",
            "1/2/3 = Filters",
            "ESC = Exit"
        ]
        y0 = 30
        for i, txt in enumerate(help_texts):
            cv2.putText(frame, txt, (10, y0 + i*30), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0,255,0), 2)
        if recording and out:
            out.write(frame)
            overlay.draw_record_indicator(frame)

        overlay.draw_info(frame, config["fps"])
        cv2.imshow("RecLite", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == 32:
            recording = not recording
            if recording:
                out, fname = recorder.init_writer(config)
                print(f"🔴 Recording started: {fname}")
            else:
                out.release()
                out = None
                print("⏹️ Recording stopped")

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

        elif key == 27:
            print("🛑 Exit program")
            break

    cap.release()
    if out:
        out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()