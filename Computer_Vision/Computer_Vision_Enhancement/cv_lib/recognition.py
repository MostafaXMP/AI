import cv2
import numpy as np

def match_object(scene_img, template_img, min_match_count=6, max_features=3000):
    scene_gray = cv2.cvtColor(scene_img, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template_img, cv2.COLOR_BGR2GRAY)

    orb = cv2.ORB_create(nfeatures=max_features)
    kp1, des1 = orb.detectAndCompute(template_gray, None)
    kp2, des2 = orb.detectAndCompute(scene_gray, None)

    if des1 is None or des2 is None:
        return scene_img.copy()

    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf.knnMatch(des1, des2, k=2)

    good_matches = []
    for m_n in matches:
        if len(m_n) == 2:
            m, n = m_n
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)

    if len(good_matches) < min_match_count:
        return cv2.drawMatches(
            template_img, kp1, scene_img, kp2, good_matches[:20], None,
            flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
        )

    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    H, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    if H is None:
        return cv2.drawMatches(
            template_img, kp1, scene_img, kp2, good_matches[:20], None,
            flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
        )

    h, w = template_gray.shape
    corners = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
    scene_corners = cv2.perspectiveTransform(corners, H)

    output = scene_img.copy()
    cv2.polylines(output, [np.int32(scene_corners)], True, (0, 255, 0), 3)
    cv2.putText(output, "Object Found", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    return output