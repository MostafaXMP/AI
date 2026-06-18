# Poisoning Attack on SVM

A demonstration of a **data poisoning attack** against a Support Vector Machine (SVM) trained on the MNIST dataset. Using the [AIJack](https://github.com/Koukyosyumei/AIJack) library, the attack injects a carefully crafted poisoned data point into the training set to degrade model accuracy — without modifying the model itself.

---

## Overview

Data poisoning attacks are a class of adversarial attacks targeting the **training phase** of a machine learning model. The attacker manipulates training data so that the model learned from that data performs worse on clean test inputs.

Unlike evasion attacks (which target inference time), poisoning attacks corrupt the learning process itself. This notebook demonstrates the full pipeline:

1. Train a binary SVM to classify digits 3 and 7 from MNIST
2. Select a training image and iteratively add adversarial noise to it
3. Re-train the SVM with the poisoned point injected
4. Compare accuracy before and after the poisoned point is added

---

## Dataset

**MNIST** — Handwritten digit images (28×28 pixels, greyscale), fetched via `sklearn.datasets.fetch_openml`.

| Split | Samples | Classes |
|---|---|---|
| Training | 5,000 | Digits 3 and 7 only |
| Validation | 500 | Digits 3 and 7 only |

- Full dataset filtered to the binary task (3 vs. 7) before splitting
- Pixel values normalised to [0, 1] by dividing by 255
- A random 100-sample subset of training data is used for the attack

---

## Project Structure

```
PoisonAttackSVM/
│
├── Copy_of_Lab_3___Poisoning_Attack___SVM.ipynb   # Main notebook
└── README.md
```

> **Note:** The MNIST dataset is downloaded automatically via `fetch_openml` on first run and cached locally in the working directory.

---

## Workflow

### 1. Environment Setup
Install required packages (shell commands included for Google Colab):
```bash
pip install aijack
# On some systems, Boost C++ libraries must be installed first — see the notebook header
```

### 2. Data Preparation
- Fetch MNIST and filter to digits `"3"` and `"7"`
- 80/20 train/validation split with shuffling
- Normalise pixel values; take 5,000/500 subsets for speed
- Labels re-encoded as `+1` (digit 7) and `-1` (digit 3) for the SVM

### 3. Train Target Model
- **SVM with linear kernel** (`sklearn.svm.SVC`)
- Evaluated on the validation set with a full classification report before any attack

### 4. Poisoning Attack
A training image of digit `"7"` is selected as the seed point. The attacker iteratively perturbs it to maximise the SVM's validation error when the poisoned point is inserted into training:

| Parameter | Value | Description |
|---|---|---|
| Seed image | 42nd "7" in training set | Starting point for the poisoned sample |
| `t` | 0.5 | Step size controlling gradient update magnitude |
| `num_iterations` | 200 | Gradient optimisation iterations |
| Training subset | 100 random samples | Subset used during the attack loop |

`attacker.attack()` returns the poisoned image and an accuracy-per-iteration log.

### 5. Visualisation
- **Attack progress plot** — shows how the model's validation accuracy degrades as the poisoned image is optimised over 200 iterations
- **Before/after images** — the original seed image vs. the final poisoned version (visually subtle changes)

### 6. Performance Comparison

| Condition | Score |
|---|---|
| Without poisoned point | Baseline accuracy on validation set |
| With poisoned point injected | Reduced accuracy after re-training |

The model is re-trained from scratch both with and without the poisoned sample to isolate the accuracy drop caused by the attack.

---

## Requirements

```
numpy
scikit-learn
matplotlib
tqdm
aijack
```

> On some systems (especially Google Colab), installing `aijack` requires Boost C++ libraries first. See the commented-out setup cells at the top of the notebook.

Install Python dependencies with:

```bash
pip install numpy scikit-learn matplotlib tqdm aijack
```

---

## Usage

1. Open the notebook:
   ```bash
   jupyter notebook Copy_of_Lab_3___Poisoning_Attack___SVM.ipynb
   ```
2. If running on **Google Colab**, uncomment and run the shell setup cells at the top.
3. Run all cells top to bottom. MNIST will be downloaded automatically on first run.

---

## Key Concepts Demonstrated

- **Data poisoning attacks** — corrupting a model by manipulating its training data
- **Threat model difference** — poisoning attacks degrade training, vs. evasion attacks which fool inference
- **Gradient-based poisoning** — iteratively optimising a seed image to maximise validation loss after re-training
- **AIJack** — privacy attack/defence library for machine learning systems
- **Accuracy degradation visualisation** — tracking how model performance drops across attack iterations
- **The vulnerability of SVMs** — even a single carefully crafted training point can measurably reduce classifier accuracy
