# MI-FACE: Model Inversion Attack on Facial Recognition

A demonstration of the **MI-FACE model inversion attack** against a neural network trained on the AT&T Faces dataset. The attack reconstructs private facial images from model outputs alone — without direct access to the training data — highlighting a critical privacy vulnerability in facial recognition systems.

---

## Overview

Model inversion (MI) attacks are a class of privacy attacks that attempt to reconstruct sensitive training data from a machine learning model's predictions. This notebook implements **MI-FACE**, a gradient-based model inversion attack specifically targeting facial recognition, using the [AIJack](https://github.com/Koukyosyumei/AIJack) library.

The workflow:
1. Train a simple classifier on 40 subjects' facial images
2. Launch a MI-FACE attack targeting a specific subject
3. Visualise the reconstructed face alongside the real training images

---

## Dataset

**AT&T Faces Dataset** (ORL Database of Faces), downloaded automatically via a companion GitHub repository.

| Property | Detail |
|---|---|
| Subjects | 40 individuals |
| Images per subject | 10 |
| Total images | 400 |
| Image format | Grayscale PGM, 112×92 pixels |
| Labels | Subject IDs 0–39 |

Images are normalised to `[-1, 1]` using mean/std of 0.5 during training.

---

## Project Structure

```
MI-FACE/
│
├── Model_Inversion.ipynb   # Main notebook
└── README.md
```

> **Note:** The AT&T Faces dataset is cloned automatically during setup from the [Facial-Similarity-with-Siamese-Networks-in-Pytorch](https://github.com/harveyslash/Facial-Similarity-with-Siamese-Networks-in-Pytorch) repository.

---

## Workflow

### 1. Environment Setup
Install required packages (shell commands included for Google Colab):
```bash
pip install aijack
# Boost C++ libraries may be required — see the notebook header
```

### 2. Model Architecture
A minimal fully connected classifier (`Net`):

| Layer | Details |
|---|---|
| Input | Flattened 112×92 grayscale image (10,304 features) |
| Fully connected | 10,304 → 40 units |
| Output | Softmax over 40 classes (one per subject) |

### 3. Training the Target Model
- Optimiser: SGD with momentum (lr=0.005, momentum=0.9)
- Loss: Cross-entropy
- Epochs: 10
- Batch size: 4
- Training accuracy reported at the end

### 4. MI-FACE Attack

The attack optimises a noise image to maximise the model's confidence for a chosen target label. Key parameters:

| Parameter | Value | Description |
|---|---|---|
| `target_label` | 11 | Subject identity to reconstruct |
| `num_itr` | 100 | Gradient optimisation iterations |
| `lam` | 0.001 | Regularisation strength (smoothness prior) |
| `log_interval` | 0 | Disable intermediate logging |

`mi.attack()` returns the reconstructed image tensor and a confidence log per iteration.

### 5. Visualisation
- **Confidence plot** — shows how the model's confidence for the target class increases over the 100 attack iterations
- **Side-by-side comparison** — the mean of all real training images for the target subject vs. the MI-FACE reconstruction

---

## Requirements

```
numpy
opencv-python
torch
torchvision
matplotlib
scikit-learn
aijack
```

> On some systems (especially Google Colab), installing `aijack` requires Boost C++ libraries first. See the commented-out setup cells at the top of the notebook.

Install Python dependencies with:

```bash
pip install numpy opencv-python torch torchvision matplotlib scikit-learn aijack
```

---

## Usage

1. Open the notebook:
   ```bash
   jupyter notebook Model_Inversion.ipynb
   ```
2. If running on **Google Colab**, uncomment and run the shell setup cells at the top.
3. Run all cells top to bottom. The dataset is cloned automatically on first run.

---

## Key Concepts Demonstrated

- **Model inversion attacks** — reconstructing private training data from model outputs
- **MI-FACE** — gradient-based inversion targeting facial recognition classifiers
- **Privacy risk in ML** — even a simple linear model leaks enough signal to approximate training images
- **AIJack** — privacy attack/defence library for machine learning systems
- **Confidence log visualisation** — tracking attack progress over iterations
- **Regularisation in MI attacks** — `lam` balances reconstruction fidelity vs. smoothness
