# features/filters.py
import cv2
import numpy as np

def _apply_contrast_brightness(bgr, alpha=1.0, beta=0.0):
    # alpha: contrast(대비), beta: brightness(밝기)
    return cv2.convertScaleAbs(bgr, alpha=alpha, beta=beta)

def _to_bgr(gray_or_bgr):
    # 입력이 그레이(2D)면 BGR로 변환해 3채널을 보장
    if len(gray_or_bgr.shape) == 2:
        return cv2.cvtColor(gray_or_bgr, cv2.COLOR_GRAY2BGR)
    return gray_or_bgr

def apply_filter(frame, mode="normal", alpha=1.2, beta=20):
    """
    mode: "normal" | "gray" | "canny" | "sepia" | "flip_h" | "flip_v"
    항상 BGR 3채널(np.uint8) 반환
    """
    # 기본 밝기/대비 먼저 적용
    img = _apply_contrast_brightness(frame, alpha=alpha, beta=beta)

    if mode == "normal":
        pass

    elif mode == "gray":
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = _to_bgr(img)

    elif mode == "canny":
        edges = cv2.Canny(img, 100, 200)
        img = _to_bgr(edges)

    elif mode == "sepia":
        # 간단한 세피아 커널
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])
        img = cv2.transform(img, kernel)
        img = np.clip(img, 0, 255).astype(np.uint8)

    elif mode == "flip_h":
        img = cv2.flip(img, 1)   # 좌우 반전

    elif mode == "flip_v":
        img = cv2.flip(img, 0)   # 상하 반전

    # 최종적으로 BGR 3채널 보장
    img = _to_bgr(img)
    return img