import cv2
import numpy as np

def create_panorama(img1, img2):

    # Ensure inputs are valid arrays
    if img1 is None or img2 is None or not isinstance(img1, np.ndarray):
        print("Error: Invalid image inputs. Expected NumPy arrays.")
        return None
    stitcher = cv2.Stitcher_create()
    status, stitched_image = stitcher.stitch([img1, img2])
    # Return the image directly if successful, otherwise return None
    if status == cv2.Stitcher_OK:
        return stitched_image
    else:
        # Status 1 = Need more images, 2 = Homography fail, 3 = Camera parameters fail
        print(f"Error: Image stitching failed with status code {status}")
        return None


def compute_depth(img_left, img_right):

    # Task 7: Estimates relative depth using stereo matching.

    # Check input images
    if img_left is None or img_right is None:
        print("Error: Invalid input images")
        return None

    # Convert images to grayscale
    gray_left = cv2.cvtColor(img_left, cv2.COLOR_BGR2GRAY)
    gray_right = cv2.cvtColor(img_right, cv2.COLOR_BGR2GRAY)

    # Reduce noise before stereo matching
    gray_left = cv2.GaussianBlur(gray_left, (5, 5), 0)
    gray_right = cv2.GaussianBlur(gray_right, (5, 5), 0)

    # Create Stereo Block Matching object
    stereo = cv2.StereoBM_create(
        numDisparities=64,
        blockSize=9
    )

    # Compute disparity map
    disparity = stereo.compute(gray_left, gray_right)

    # Normalize disparity for visualization
    disparity_norm = cv2.normalize(
        disparity,
        None,
        alpha=0,
        beta=255,
        norm_type=cv2.NORM_MINMAX,
        dtype=cv2.CV_8U
    )

    # Remove salt-and-pepper noise
    disparity_norm = cv2.medianBlur(disparity_norm, 5)

    return disparity_norm

