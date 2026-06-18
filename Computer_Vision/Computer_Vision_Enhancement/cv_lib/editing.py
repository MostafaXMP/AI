import cv2
import numpy as np

def selective_enhance(image, target_ranges, 
                     sharpen_strength=1.5, 
                     blur_size=(21, 21),
                     feather_size=11):

    """
    target_ranges: list of (lower, upper) HSV ranges
                   e.g. [(lower_red1, upper_red1), (lower_red2, upper_red2)]
    """

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # --- Build combined mask ---
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    for lower, upper in target_ranges:
        mask |= cv2.inRange(hsv, lower, upper)

    # --- Clean mask ---
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # --- Feather mask (smooth edges for better blending) ---
    mask = cv2.GaussianBlur(mask, (feather_size, feather_size), 0)
    mask_3d = cv2.merge([mask, mask, mask]).astype(np.float32) / 255.0

    # --- Sharpen only once ---
    blurred_small = cv2.GaussianBlur(image, (0, 0), 2)
    sharpened = cv2.addWeighted(image, 1 + sharpen_strength, blurred_small, -sharpen_strength, 0)

    # --- Background blur ---
    background_blurred = cv2.GaussianBlur(image, blur_size, 0)

    # --- Final blend ---
    enhanced = (sharpened.astype(np.float32) * mask_3d +
                background_blurred.astype(np.float32) * (1 - mask_3d))

    return np.clip(enhanced, 0, 255).astype(np.uint8)