import cv2
import datetime
import numpy as np

def draw_record_indicator(frame):
    cv2.circle(frame, (50, 50), 15, (0, 0, 255), -1)
    cv2.putText(frame, "REC", (80, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

def draw_info(frame, fps):
    h, w = frame.shape[:2]
    fs = max(0.55, min(1.0, w / 1280 * 0.7))
    th = 2 if w >= 900 else 1
    now = datetime.datetime.now().strftime("%H:%M:%S")
    cv2.putText(frame, f"FPS: {fps}", (10, int(24*fs)+8),
                cv2.FONT_HERSHEY_SIMPLEX, fs, (255, 255, 0), th, cv2.LINE_AA)
    cv2.putText(frame, f"Time: {now}", (10, int(24*fs)*2 + 16),
                cv2.FONT_HERSHEY_SIMPLEX, fs, (255, 255, 255), th, cv2.LINE_AA)

def draw_help(frame, recording, filter_mode, source_idx, total_sources):
    h, w = frame.shape[:2]
    pad = max(8, int(w * 0.01))
    fs_main = max(0.7, min(1.3, w / 1280 * 0.9))
    fs_sub = max(0.6, min(1.1, w / 1280 * 0.8))
    th_main = 2 if w >= 900 else 1
    th_sub = th_main

    lines = [
        "SPACE = Record/Stop",
        "S=Screenshot   1-6=Filters   TAB=Switch Source   ESC=Exit",
        f"Source: {source_idx+1}/{total_sources}   Mode: {'REC' if recording else 'PREVIEW'}   Filter: {filter_mode}",
    ]

    sizes0 = cv2.getTextSize(lines[0], cv2.FONT_HERSHEY_SIMPLEX, fs_main, th_main)[0]
    sizes_rest = [cv2.getTextSize(t, cv2.FONT_HERSHEY_SIMPLEX, fs_sub, th_sub)[0] for t in lines[1:]]
    line_h0 = int(sizes0[1] * 1.4)
    line_hs = [int(s[1] * 1.4) for s in sizes_rest]
    bar_h = pad + line_h0 + sum(line_hs) + pad

    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, bar_h), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.35, frame, 0.65, 0, frame)

    x = pad
    y = pad + line_h0 - int(line_h0 * 0.35)
    cv2.putText(frame, lines[0], (x, y), cv2.FONT_HERSHEY_SIMPLEX, fs_main, (0, 255, 255), th_main, cv2.LINE_AA)

    y += line_h0
    cv2.putText(frame, lines[1], (x, y), cv2.FONT_HERSHEY_SIMPLEX, fs_sub, (0, 255, 0), th_sub, cv2.LINE_AA)

    y += line_hs[0]
    cv2.putText(frame, lines[2], (x, y), cv2.FONT_HERSHEY_SIMPLEX, fs_sub, (0, 255, 0), th_sub, cv2.LINE_AA)


def draw_filters_bar(frame):
    h, w = frame.shape[:2]
    pad = max(8, int(w * 0.01))
    fs = max(0.5, min(1.2, w / 1280 * 0.7))
    th = 2 if w >= 900 else 1

    lines = [
        "Filters: 1=Normal  2=Gray  3=Canny  4=Sepia  5=FlipH  6=FlipV",
    ]

    txt_sizes = [cv2.getTextSize(t, cv2.FONT_HERSHEY_SIMPLEX, fs, th)[0] for t in lines]
    line_h = int(max(s[1] for s in txt_sizes) * 1.4)
    bar_h = line_h * len(lines) + pad * 2
    y0 = h - bar_h

    overlay = frame.copy()
    cv2.rectangle(overlay, (0, y0), (w, h), (0, 0, 0), -1)
    alpha = 0.35
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    y = y0 + pad + line_h - int(line_h * 0.35)
    x = pad
    for i, t in enumerate(lines):
        cv2.putText(frame, t, (x, y + i * line_h), cv2.FONT_HERSHEY_SIMPLEX, fs, (0, 255, 255), th, cv2.LINE_AA)