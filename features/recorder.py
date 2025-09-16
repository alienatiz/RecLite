# features/recorder.py
import os
import cv2
import datetime

def _ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def init_writer(config: dict, filename: str | None = None):
    out_dir = config.get("output_dir", "outputs")
    _ensure_dir(out_dir)

    fourcc_code = config.get("codec", "XVID")
    fourcc = cv2.VideoWriter_fourcc(*fourcc_code)

    fps = float(config.get("fps", 20.0))
    width = int(config.get("frame_width", 640))
    height = int(config.get("frame_height", 480))

    if not filename:
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(out_dir, f"output_{ts}.avi")

    writer = cv2.VideoWriter(filename, fourcc, fps, (width, height))
    if not writer.isOpened():
        raise RuntimeError(f"[recorder] Failed to open VideoWriter for: {filename}")
    return writer, filename

def close_writer(writer):
    if writer is not None:
        writer.release()