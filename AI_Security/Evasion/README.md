# Evasion Attack on SVM

An adversarial machine learning project demonstrating an **evasion attack** against a Support Vector Machine (SVM) classifier trained on the MNIST dataset. Using the [AIJack](https://github.com/Koukyosyumei/AIJack) library, the project crafts adversarial examples that cause a digit classifier to misclassify a handwritten **7** as a **3** — with minimal visible change to the image.

---

## Overview

Evasion attacks are a class of adversarial attacks where an attacker manipulates an input **at inference time** to fool a trained model, without modifying the model itself. This notebook demonstrates the full pipeline:

1. Train a binary SVM to distinguish digits 3 and 7
2. Mount an evasion attack using AIJack to perturb a "7" sample
3. Confirm the adversarial example is misclassified as "3"
4. Visually compare the original vs. adversarial image side by side

---

## Dataset

**MNIST** — Handwritten digit images (28×28 pixels, greyscale), fetched via `sklearn.datasets.fetch_openml`.

| Split | Samples | Classes |
|---|---|---|
| Training | 5,000 | Digits 3 and 7 only |
| Validation | 500 | Digits 3 and 7 only |

- Pixel values normalised to [0, 1] by dividing by 255
- Full dataset filtered to the binary task (3 vs. 7) before splitting

---

## Project Structure

```
EvasionAttackSVM/
│
├── Evasion_attack_on_SVM.ipynb   # Main notebook
└── README.md
```

> **Note:** The MNIST dataset is downloaded automatically via `fetch_openml` on first run and cached locally in the working directory.

---

## Workflow

### 1. Environment Setup
Install required packages (commented-out shell commands included for Google Colab):
```bash
pip install aijack
# On some systems, Boost libraries must be installed first — see the notebook header
```

### 2. Data Preparation
- Fetch MNIST (70,000 samples, 784 features each)
- Filter to digits `"3"` and `"7"` only
- 80/20 train/validation split with shuffling
- Normalise pixel values; take a 5,000/500 subset for training speed

### 3. Train Target Model
- **SVM with linear kernel** (`sklearn.svm.SVC`)
- Evaluated on the validation set with a full classification report (precision, recall, F1)

### 4. Evasion Attack

The attacker is initialised with the following key parameters:

| Parameter | Value | Description |
|---|---|---|
| `X_minus_1` | All "3" training samples | Samples of the class the attacker wants to impersonate |
| `dmax` | `(5000 / 255) × 2.5` | Max allowed perturbation per feature |
| `max_iter` | 300 | Maximum optimisation iterations |
| `gamma` | `1 / (features × var(X))` | Perturbation magnitude scaling |
| `lam` | 10 | Regularisation strength |
| `t` | 0.5 | Trade-off between perturbation size and attack success |
| `h` | 10 | Step size during gradient-based optimisation |

A seed sample (a "7" from the validation set) is fed into the attacker, which iteratively perturbs it until the SVM predicts "3".

### 5. Visualisation
Side-by-side plot of the original and adversarial images, with the SVM's prediction shown as the title of each subplot.

---

## Requirements

```
numpy
scikit-learn
matplotlib
aijack
```

> On some systems (especially Google Colab), installing `aijack` requires Boost C++ libraries first. See the commented-out setup cells at the top of the notebook.

Install Python dependencies with:

```bash
pip install numpy scikit-learn matplotlib aijack
```

---

## Usage

1. Open the notebook:
   ```bash
   jupyter notebook Evasion_attack_on_SVM.ipynb
   ```
2. If running on **Google Colab**, uncomment and run the shell setup cells at the top to install `aijack` and its dependencies.
3. Run all cells top to bottom. MNIST will be downloaded automatically on first run.

---

## Key Concepts Demonstrated

- Adversarial machine learning — evasion attacks at inference time
- Binary SVM classification on image data
- Gradient-based adversarial perturbation using AIJack
- Perturbation budget constraint (`dmax`) to keep changes imperceptible
- Visual inspection of original vs. adversarial examples
- The vulnerability of linear SVMs to carefully crafted inputs
