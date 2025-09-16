import cv2
import datetime
import os

def save_screenshot(frame, output_dir="outputs"):
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(output_dir, f"screenshot_{now}.jpg")
    cv2.imwrite(filename, frame)
    print(f"📸 Screenshot saved: {filename}")