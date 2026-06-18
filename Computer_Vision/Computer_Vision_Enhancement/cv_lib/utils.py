import cv2
import matplotlib.pyplot as plt
from PIL import Image


def load_image(path):
    img = cv2.imread(path)
    if img is None:
        raise ValueError(f"Image at {path} not found.")
    return img

def to_rgb(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def to_hsv(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

def show_images(images, titles, figsize=(15, 10)):
    n = len(images)
    plt.figure(figsize=figsize)
    for i in range(n):
        plt.subplot(1, n, i + 1)
        if len(images[i].shape) == 2:
            plt.imshow(images[i], cmap='gray')
        else:
            plt.imshow(to_rgb(images[i]))
        plt.title(titles[i])
        plt.axis('off')
    plt.show()



def get_exposure_times(list_of_paths):
    exposure_times = []
    for path in list_of_paths: # Loop through the list directly
        img = Image.open(path)
        exif = img.getexif()
        # Access the Exif IFD (0x8769)
        ifd = exif.get_ifd(0x8769)
        # 33434 is the ExposureTime tag
        raw_time = ifd.get(33434)
        if raw_time is not None:
            exposure_times.append(round(float(raw_time),5))
        else:
            print(f"Warning: No exposure time found for {path}")
            
    return exposure_times


def split_image_vertical(image):
    h, w = image.shape[:2]
    
    mid = w // 2  # middle column
    
    left_half = image[:, :mid+100]
    right_half = image[:, mid-100:]
    show_images([left_half, right_half], ["Left Half", "Right Half"])
    return left_half, right_half