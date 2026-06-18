# IrisClassify — SVM & Neural Network Comparison on the Iris Dataset

A machine learning project that benchmarks **Support Vector Machines (SVM)** and **feedforward Neural Networks** for multi-class flower species classification using the classic Iris dataset.

---

## Overview

This notebook explores and compares two fundamentally different ML approaches on the same classification task:

- **SVM** with three kernel types (Linear, Polynomial, RBF)
- **Neural Networks** with three activation function combinations (ReLU/Softmax, Sigmoid/Softmax, ReLU/Sigmoid)

The goal is to understand how kernel choice and activation functions affect classification performance on a well-understood dataset.

---

## Dataset

**Iris Dataset** (`Iris.csv`)

| Feature | Description |
|---|---|
| SepalLengthCm | Sepal length in centimetres |
| SepalWidthCm | Sepal width in centimetres |
| PetalLengthCm | Petal length in centimetres |
| PetalWidthCm | Petal width in centimetres |
| Species | Target class (Iris-setosa / Iris-versicolor / Iris-virginica) |

- 150 samples (duplicates removed)
- 3 target classes
- 4 numerical features

---

## Project Structure

```
IrisClassify/
│
├── v2MachineLearning3Snapshot.ipynb   # Main notebook
├── Iris.csv                           # Dataset
└── README.md
```

---

## Workflow

### 1. Data Preprocessing
- Null and duplicate checks (duplicates dropped)
- Feature/target split (`X` = 4 features, `y` = Species)
- Label encoding of target classes
- 70/30 train-test split (`random_state=42`)

### 2. Exploratory Data Analysis
- Feature distribution histograms
- Pairplot coloured by species (seaborn)

### 3. SVM Models
Three kernels are trained and evaluated independently:

| Kernel | Notes |
|---|---|
| Linear | Best for linearly separable classes |
| Polynomial (`poly`) | Captures non-linear boundaries via polynomial mapping |
| RBF (Radial Basis Function) | General-purpose non-linear kernel |

Each model is assessed with a classification report and confusion matrix.

### 4. Neural Network Models
A Sequential Keras model with 2 hidden layers (10 → 8 → 3 units) is tested with three activation configurations:

| Configuration | Hidden Layers | Output Layer |
|---|---|---|
| ReLU + Softmax | ReLU | Softmax |
| Sigmoid + Softmax | Sigmoid | Softmax |
| ReLU + Sigmoid | ReLU | Sigmoid |

All models use the **Adam** optimiser, **sparse categorical cross-entropy** loss, and **early stopping** (patience = 3, monitored on training loss) to prevent unnecessary epochs.

---

## Requirements

```
numpy
pandas
matplotlib
seaborn
scikit-learn
tensorflow / keras
```

Install all dependencies with:

```bash
pip install numpy pandas matplotlib seaborn scikit-learn tensorflow
```

---

## Usage

1. Clone the repository and place `Iris.csv` in the project root.
2. Open the notebook:
   ```bash
   jupyter notebook v2MachineLearning3Snapshot.ipynb
   ```
3. Run all cells top to bottom. EarlyStopping means training halts automatically once the loss stops improving.

---

## Key Concepts Demonstrated

- Multi-class classification with SVM and deep learning
- Effect of SVM kernel choice on decision boundaries
- Comparison of activation functions in neural networks
- Label encoding vs. one-hot encoding
- Evaluation via confusion matrices and classification reports (precision, recall, F1)
