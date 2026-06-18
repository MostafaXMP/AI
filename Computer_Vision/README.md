# cv-toolkit

A modular computer vision library built on top of OpenCV, covering eight image processing tasks — from intelligent auto-enhancement and document cleaning to HDR fusion, panorama stitching, depth estimation, and object recognition. All functionality is organised into focused modules and driven by a single `main.py` demo script.

---

## Project Structure

```
cv-toolkit/
│
├── cv_lib/
│   ├── __init__.py
│   ├── editing.py        # Task 1 — Selective colour enhancement
│   ├── enhancement.py    # Tasks 2, 3, 8 — Sharpening, auto-enhance, HDR
│   ├── geometry.py       # Tasks 5, 7 — Panorama stitching, depth estimation
│   ├── recognition.py    # Task 6 — Feature-based object recognition
│   ├── document.py       # Task 4 — Scanned document cleaning
│   └── utils.py          # Image I/O, display helpers, EXIF reader
│
├── main.py               # End-to-end demo of all 8 tasks
└── README.md
```

---

## Tasks & Modules

### Task 1 — Selective Colour Enhancement (`editing.py`)
Sharpens a user-defined colour region (specified as HSV ranges) while softly blurring the background, drawing the viewer's eye to the subject.

- Builds a combined HSV mask for multi-range colours (e.g. both red hue wraps)
- Cleans the mask with morphological opening, then feathers edges with Gaussian blur
- Blends a sharpened foreground against a blurred background using the soft mask

### Task 2 — Sharpening Pipelines (`enhancement.py`)
Three classical sharpening methods, each operating in a different way:

| Pipeline | Method |
|----------|--------|
| `pipeline_laplacian` | Subtracts the Laplacian from the L channel in LAB space |
| `pipeline_highboost` | Adds a scaled high-frequency mask back to the image |
| `pipeline_unsharp_mask` | Amplifies detail via unsharp masking with tunable sigma and strength |

### Task 3 — Intelligent Auto Enhancement (`enhancement.py`)
Analyses an image and applies only the corrections it actually needs:

| Metric | Correction Applied |
|--------|--------------------|
| Low brightness (< 85) | Gamma correction γ = 0.35 (brighten) |
| High brightness (> 170) | Gamma correction γ = 2.2 (darken) |
| Low contrast (std < 50) | CLAHE on the L channel (LAB) |
| Low saturation (< 120) | HSV saturation boost (1.15×–1.30×) |
| High noise (Laplacian var > 500) | Non-local means denoising |

### Task 4 — Document Cleaning (`document.py`)
Restores scanned documents degraded by noise and uneven lighting:

1. Non-local means denoising on the grayscale image
2. Adaptive Gaussian thresholding to handle varying illumination
3. Morphological opening to remove residual speckle

### Task 5 — Panorama Stitching (`geometry.py`)
Stitches two overlapping images into a single wide-angle panorama using OpenCV's built-in `Stitcher`, which handles feature detection, homography estimation, and warping internally.

### Task 6 — Object Recognition (`recognition.py`)
Locates a template object inside a scene image using ORB feature matching:

1. Detects keypoints with ORB (up to 3000 features per image)
2. Matches descriptors with brute-force Hamming distance + Lowe's ratio test (0.75)
3. Estimates a homography with RANSAC and draws the detected object boundary

### Task 7 — Depth Estimation (`geometry.py`)
Produces a relative depth map from a stereo image pair using block matching:

1. Pre-blurs both channels to reduce noise before matching
2. Runs `StereoBM` (64 disparities, block size 9)
3. Normalises and median-filters the disparity map for clean visualisation

### Task 8 — HDR Imaging (`enhancement.py`)
Fuses multiple exposures into a single high-dynamic-range image using Mertens Exposure Fusion. Two modes are provided:

| Function | Use case |
|----------|----------|
| `create_hdr` | Handheld shots — aligns frames first using AKAZE feature matching + RANSAC homography |
| `create_hdr2` | Tripod shots — skips alignment, fuses directly for cleaner results |

---

## Requirements

- Python 3.7+
- OpenCV (`opencv-contrib-python` recommended for AKAZE support)
- NumPy
- Matplotlib
- Pillow

Install dependencies:

```bash
pip install opencv-contrib-python numpy matplotlib Pillow
```

---

## Usage

Place your images in the project root (see expected filenames below) and run:

```bash
python main.py
```

### Expected input files

| File | Used by |
|------|---------|
| `image1.webp` | Tasks 1, 2, 3, 4, 5, 6, 7 |
| `template.jpeg` | Task 6 (crop of the object to find) |
| `HDR_images/1.jpg`, `2.jpg`, `3.jpg` | Task 8 — handheld HDR set |
| `HDR_images/13.jpg` … `16.jpg` | Task 8 — tripod HDR set |

HDR images must have EXIF exposure time metadata for `get_exposure_times()` to work.

---

## Module Reference

| Module | Key functions |
|--------|--------------|
| `editing` | `selective_enhance(image, target_ranges, ...)` |
| `enhancement` | `pipeline_laplacian`, `pipeline_highboost`, `pipeline_unsharp_mask`, `intelligent_enhance`, `create_hdr`, `create_hdr2` |
| `geometry` | `create_panorama(img1, img2)`, `compute_depth(img_left, img_right)` |
| `recognition` | `match_object(scene_img, template_img, ...)` |
| `document` | `clean_document(image)` |
| `utils` | `load_image`, `show_images`, `to_rgb`, `to_hsv`, `get_exposure_times`, `split_image_vertical` |

---

## Key Concepts

| Concept | Description |
|---------|-------------|
| **HSV masking** | Isolating colour regions by hue, saturation, and value ranges |
| **CLAHE** | Contrast-Limited Adaptive Histogram Equalisation — boosts local contrast without over-amplifying noise |
| **Unsharp masking** | Sharpening by amplifying the difference between an image and its blurred version |
| **AKAZE / ORB** | Binary feature detectors robust to scale, rotation, and exposure change |
| **Homography** | A perspective transformation matrix mapping one image plane to another |
| **StereoBM** | Block-matching stereo algorithm that finds corresponding pixels between left/right views to estimate depth |
| **Mertens fusion** | Exposure fusion technique that blends multi-exposure images by weighting contrast, saturation, and well-exposedness |
