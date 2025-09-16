import cv2
import numpy as np

def _apply_contrast_brightness(bgr, alpha=1.0, beta=0.0):
    return cv2.convertScaleAbs(bgr, alpha=alpha, beta=beta)

def _to_bgr(img):
    if len(img.shape) == 2:
        return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    return img.astype("uint8")

def apply_filter(frame, mode="normal", alpha=1.2, beta=20):
    img = _apply_contrast_brightness(frame, alpha=alpha, beta=beta)

    state = 1
    if mode == "normal":
        img = cv2.flip(img, state)
    elif mode == "gray":
        if state == 0:
            img = cv2.flip(img, state)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = _to_bgr(img)
        if state == 1:
            img = cv2.flip(img, state)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = _to_bgr(img)
    elif mode == "canny":
        if state == 0:
            img = cv2.flip(img, state)
            edges = cv2.Canny(img, 100, 200)
            img = _to_bgr(edges)
        if state == 1:
            img = cv2.flip(img, state)
            edges = cv2.Canny(img, 100, 200)
            img = _to_bgr(edges)
    elif mode == "sepia":
        if state == 0:
            img = cv2.flip(img, state)
            kernel = np.array([[0.272, 0.534, 0.131],
                            [0.349, 0.686, 0.168],
                            [0.393, 0.769, 0.189]])
            img = cv2.transform(img, kernel)
            img = np.clip(img, 0, 255).astype(np.uint8)
        if state == 1:
            img = cv2.flip(img, state)
            kernel = np.array([[0.272, 0.534, 0.131],
                            [0.349, 0.686, 0.168],
                            [0.393, 0.769, 0.189]])
            img = cv2.transform(img, kernel)
            img = np.clip(img, 0, 255).astype(np.uint8)
    elif mode == "flip_h":
        if state == 0:
            img = cv2.flip(img, 1)
        if state == 1:
            img = cv2.flip(img, 1)
    elif mode == "flip_v":
        if state == 0:
            img = cv2.flip(img, 0)
        if state == 1:
            img = cv2.flip(img, 0)

    img = _to_bgr(img)
    return img