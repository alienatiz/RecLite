import cv2
import datetime

def draw_record_indicator(frame):
    cv2.circle(frame, (50, 50), 15, (0, 0, 255), -1)
    cv2.putText(frame, "REC", (80, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

def draw_info(frame, fps):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    cv2.putText(frame, f"Time: {now}", (10, frame.shape[0]-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    cv2.putText(frame, f"FPS: {fps}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 1)

def draw_help(frame, recording, filter_mode, source_idx, total_sources):
    lines = [
        "SPACE=Record/Stop  S=Screenshot  1-6=Filters  TAB=Switch Source  ESC=Exit",
        f"Source: {source_idx+1}/{total_sources}  Mode: {'REC' if recording else 'PREVIEW'}  Filter: {filter_mode}"
    ]
    y = 70
    for i, txt in enumerate(lines):
        cv2.putText(frame, txt, (10, y + i*28),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)