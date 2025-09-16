import os
import cv2
import datetime

def init_writer(config, filename=None):
    out_dir = config.get("output_dir", "outputs")
    os.makedirs(out_dir, exist_ok=True)

    pref_codec = str(config.get("codec", "mp4v")).strip()
    pref_ext = str(config.get("output_ext", ".mp4")).strip()

    codec_chain = [
        (pref_codec, pref_ext),
        ("mp4v", ".mp4"),
        ("avc1", ".mp4"),
        ("MJPG", ".avi"), 
    ]

    fps = float(config.get("fps", 20.0))
    width = int(config.get("frame_width", 640))
    height = int(config.get("frame_height", 480))

    if width <= 0 or height <= 0:
        raise ValueError("[recorder] Invalid frame size in config: width/height must be > 0")

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    base = os.path.join(out_dir, f"output_{ts}")

    last_err = None
    for fourcc_code, ext in codec_chain:
        try:
            target = filename if filename else base + ext
            fourcc = cv2.VideoWriter_fourcc(*fourcc_code)
            writer = cv2.VideoWriter(target, fourcc, fps, (width, height))
            if writer.isOpened():
                return writer, target
            else:
                last_err = f"VideoWriter not opened for {target} with codec {fourcc_code}"
        except Exception as e:
            last_err = str(e)

    raise RuntimeError(f"Failed to open VideoWriter. Last error: {last_err}")