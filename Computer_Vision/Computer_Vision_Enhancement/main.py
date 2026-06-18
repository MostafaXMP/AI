import cv2
import numpy as np
from cv_lib import enhancement, recognition, utils, editing, document, geometry

def main():
    # Load sample image
    image = utils.load_image("image1.webp")
    
    # --- Task 1: Selective Enhancement ---
    red_ranges = [
    (np.array([0,120,70]), np.array([10,255,255])),
    (np.array([170,120,70]), np.array([180,255,255]))
    ]

    result = editing.selective_enhance(image, red_ranges)
    utils.show_images([image, result], ["Original", "Task 1: Selective Enhancement"])


    # --- Task 2: Sharpening Pipelines ---
    laplacian = enhancement.pipeline_laplacian(image)
    highboost = enhancement.pipeline_highboost(image)
    unsharp = enhancement.pipeline_unsharp_mask(image)
    utils.show_images([image, laplacian, highboost, unsharp], 
                      ["Original", "Laplacian", "High-boost", "Unsharp Mask"])
    
    # --- Task 3: Intelligent Auto Enhancement ---
    dark_image   = np.clip(image.astype(np.int32) - 100, 0, 255).astype(np.uint8)
    bright_image = np.clip(image.astype(np.int32) + 100, 0, 255).astype(np.uint8)

    print("--- Dark ---");   dark_r   = enhancement.intelligent_enhance(dark_image)
    print("--- Bright ---"); bright_r = enhancement.intelligent_enhance(bright_image)
    print("--- Normal ---"); normal_r = enhancement.intelligent_enhance(image)

    utils.show_images(
    [dark_image, dark_r, bright_image, bright_r, image, normal_r],
    ["Dark Input", "Brightened",
    "Bright Input", "Darkened",
    "Normal Input", "CLAHE"],
    )

    task3_result = enhancement.intelligent_enhance(image)
    utils.show_images([image, task3_result], ["Original", "Task 3: Auto Enhancement"])
    
    # --- Task 4: Document Cleaning ---
    task4_result = document.clean_document(image)
    utils.show_images([image, task4_result], ["Original", "Task 4: Cleaned Document"])
    
    print("Demo complete. Results displayed.")

    # --- Task 5: Image Stitching ---
    left_half, right_half = utils.split_image_vertical(image)
    task5_result = geometry.create_panorama(left_half, right_half)
    utils.show_images([task5_result], ["Stitched Panorama"])

    # --- Task 6: Object Recognition ---
    template_img = utils.load_image("template.jpeg")   # crop of one rose or one clear object
    scene_img = utils.load_image("image1.webp")         # image containing the same object

    task6_result = recognition.match_object(scene_img, template_img, min_match_count=6, max_features=5000)   
    utils.show_images([scene_img, task6_result], ["Scene", "Task 6: Transformed Object Recognition"])

    # # --- Task 7: Depth Estimation ---
    task7_result = geometry.compute_depth(left_half, right_half)  # Using same image for demo
    utils.show_images([image, task7_result], ["Original", "Task 7: Depth Estimation"])


    # # --- Task 8: HDR ---
    images_paths = ["HDR_images/1.jpg", "HDR_images/2.jpg", "HDR_images/3.jpg"]  # Sample images with different exposures
    exposure_times = utils.get_exposure_times(images_paths)
    print(exposure_times)
    images = [cv2.imread(path) for path in images_paths]
    task82_result = enhancement.create_hdr(images, exposure_times)  # Using same image for demo
    utils.show_images([images[0], images[1], images[2], task82_result], ["1", "2", "3", "Task 8: HDR Image"])
    # cv2.imwrite('output1.jpg', task82_result)

    images_paths = ["HDR_images/16.jpg", "HDR_images/15.jpg", "HDR_images/14.jpg", "HDR_images/13.jpg",]  # Sample images with different exposures
    exposure_times = utils.get_exposure_times(images_paths)
    print(exposure_times)
    images = [cv2.imread(path) for path in images_paths]
    task81_result = enhancement.create_hdr2(images, exposure_times)  # Using same image for demo
    utils.show_images([images[0], images[1], images[2], images[3], task81_result], ["1", "2", "3", "4", "Task 8: HDR Image"])
    #cv2.imwrite('output1.jpg', task82_result)



if __name__ == "__main__":
    main()
