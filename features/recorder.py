import cv2
import datetime
import os

def init_writer(config):
    fourcc = cv2.VideoWriter_fourcc(*config["codec"])
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(config["output_dir"], f"output_{now}.avi")
    return cv2.VideoWriter(
        filename,
        fourcc,
        config["fps"],
        (config["frame_width"], config["frame_height"])
    ), filename