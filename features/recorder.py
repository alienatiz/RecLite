import os
import cv2
import datetime

def init_writer(config, filename=None):
    out_dir = config.get("output_dir", "outputs")
    os.makedirs(out_dir, exist_ok=True)

    fourcc = cv2.VideoWriter_fourcc(*config.get("codec", "mp4v"))
    fps = float(config.get("fps", 20.0))

    width = int(config.get("frame_width", 640))
    height = int(config.get("frame_height", 480))

    if not filename:
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        ext = config.get("output_ext", ".mp4")
        filename = os.path.join(out_dir, f"output_{ts}{ext}")

    writer = cv2.VideoWriter(filename, fourcc, fps, (width, height))
    if not writer.isOpened():
        raise RuntimeError(f"[recorder] Failed to open VideoWriter for {filename}")
    return writer, filename