import cv2
import numpy as np

# Task 2: Sharpening Pipelines
def pipeline_laplacian(image):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    L, A, B = cv2.split(lab)
    L = L.astype(np.float32)
    laplacian = cv2.Laplacian(L, cv2.CV_32F)
    L_sharp = L - laplacian
    L_sharp = np.clip(L_sharp, 0, 255).astype(np.uint8)
    merged = cv2.merge((L_sharp, A, B))
    return cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)

def pipeline_highboost(image, k=1.5):
    image_f = image.astype(np.float32)
    blurred = cv2.GaussianBlur(image_f, (5, 5), 0)
    mask = image_f - blurred
    sharpened = image_f + k * mask
    return np.clip(sharpened, 0, 255).astype(np.uint8)

def pipeline_unsharp_mask(image, sigma=1.0, strength=1.5):
    image_f = image.astype(np.float32)
    blurred = cv2.GaussianBlur(image_f, (0, 0), sigma)
    sharpened = image_f + strength * (image_f - blurred)
    return np.clip(sharpened, 0, 255).astype(np.uint8)

# Task 3: Intelligent Auto Image Enhancement

def intelligent_enhance(image):
    img = image.copy()
    h_orig, w_orig = img.shape[:2]

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Image Analysis
    non_white = gray < 235
    mean_val  = float(np.mean(gray[non_white])) if non_white.any() else float(np.mean(gray))
    std_val   = float(np.std(gray[non_white]))  if non_white.any() else float(np.std(gray))
    avg_noise = float(cv2.Laplacian(gray, cv2.CV_64F).var())

    print(f"Brightness : {mean_val:.1f}")
    print(f"Contrast   : {std_val:.1f}")
    print(f"Noise      : {avg_noise:.1f}")

    enhanced = img.copy()

    # Brightness Correction
    def gamma_lut(gamma):
        lut = np.arange(256, dtype=np.float32)
        lut = ((lut / 255.0) ** gamma) * 255.0
        return np.clip(lut, 0, 255).astype(np.uint8)

    if mean_val < 85:
        print("→ Fix: Brighten (γ=0.35)")
        enhanced = cv2.LUT(enhanced, gamma_lut(0.35))
    elif mean_val > 170:
        print("→ Fix: Darken (γ=2.2)")
        enhanced = cv2.LUT(enhanced, gamma_lut(2.2))
    else:
        print("→ Brightness OK")

    # Contrast Correction
    if std_val < 50:
        print("→ Fix: CLAHE (low contrast)")
        l, a, b = cv2.split(cv2.cvtColor(enhanced, cv2.COLOR_BGR2LAB))
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        enhanced = cv2.cvtColor(cv2.merge((l, a, b)), cv2.COLOR_LAB2BGR)
    else:
        print("→ Contrast OK")

    # Saturation Correction
    hsv_e   = cv2.cvtColor(enhanced, cv2.COLOR_BGR2HSV).astype(np.float32)
    avg_sat = float(np.mean(hsv_e[:,:,1]))
    print(f"Saturation : {avg_sat:.1f}")

    if avg_sat < 80:
        boost = 1.3
        print(f"→ Fix: Saturation boost x{boost} (dull colors)")
    elif avg_sat < 120:
        boost = 1.15
        print(f"→ Fix: Saturation boost x{boost} (slightly dull)")
    else:
        boost = 1.0
        print("→ Saturation OK")

    if boost > 1.0:
        hsv_e[:,:,1] = np.clip(hsv_e[:,:,1] * boost, 0, 255)
        enhanced = cv2.cvtColor(hsv_e.astype(np.uint8), cv2.COLOR_HSV2BGR)

    # Noise Reduction
    if avg_noise > 500:
        print("→ Fix: Denoise (noisy image)")
        enhanced = cv2.fastNlMeansDenoisingColored(enhanced, None, h=3, hColor=3,
                                                    templateWindowSize=5, searchWindowSize=21)
    else:
        print("→ Noise OK")

    if enhanced.shape[:2] != (h_orig, w_orig):
        enhanced = cv2.resize(enhanced, (w_orig, h_orig))

    return enhanced


# Task 8: HDR Imaging
def align_images_akaze(images):
    """Aligns images using AKAZE, which is highly robust for varying exposures."""
    ref_img = images[0]
    ref_gray = cv2.cvtColor(ref_img, cv2.COLOR_BGR2GRAY)
    aligned_images = [ref_img]

    # Initialize AKAZE detector
    akaze = cv2.AKAZE_create()
    kp1, des1 = akaze.detectAndCompute(ref_gray, None)
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)

    for i in range(1, len(images)):
        img = images[i]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        kp2, des2 = akaze.detectAndCompute(gray, None)

        # Match features
        matches = matcher.match(des2, des1)
        matches = sorted(matches, key=lambda x: x.distance)

        # Keep only the top 15% matches to filter out the dark sky noise
        good_matches = matches[:int(len(matches) * 0.15)]

        if len(good_matches) < 10:
            print(f"Warning: Not enough features for image {i}. Skipping alignment.")
            aligned_images.append(img)
            continue

        # Extract coordinates
        src_pts = np.float32([kp2[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp1[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

        # Find Homography using RANSAC
        H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        if H is not None:
            # Warp the image to align perfectly with the first image
            h, w = ref_img.shape[:2]
            aligned_img = cv2.warpPerspective(img, H, (w, h))
            aligned_images.append(aligned_img)
        else:
            aligned_images.append(img)

    return aligned_images

def create_hdr(images, exposure_times=None):
    # 1. Advanced Alignment (Fixes camera shake and rotation)
    print("Aligning images using AKAZE feature matching...")
    aligned_images = align_images_akaze(images)

    # 2. Merge using Mertens (Best for colors in handheld shots)
    print("Merging using Mertens Exposure Fusion...")
    merge_mertens = cv2.createMergeMertens()
    fusion = merge_mertens.process(aligned_images)

    # 3. Convert and Save
    ldr_8bit = np.clip(fusion * 255, 0, 255).astype(np.uint8)

    return ldr_8bit

def create_hdr2(images, exposure_times=None):
    # 1. Skip alignment. The tripod already did the work!
    
    # 2. Merge using Mertens (Handles colors beautifully)
    merge_mertens = cv2.createMergeMertens()
    fusion = merge_mertens.process(images)

    # 3. Convert and Save
    ldr_8bit = np.clip(fusion * 255, 0, 255).astype(np.uint8)

    return ldr_8bit