import cv2
import datetime

def draw_record_indicator(frame):
    cv2.circle(frame, (50, 50), 15, (0, 0, 255), -1)
    cv2.putText(frame, "REC", (80, 60), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 255), 2)

def draw_info(frame, fps):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    cv2.putText(frame, f"Time: {now}", (10, frame.shape[0]-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    cv2.putText(frame, f"FPS: {fps}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 1)