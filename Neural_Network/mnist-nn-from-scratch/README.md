# 🔢 Digit Recognizer — Neural Network from Scratch (NumPy + SGD)

A fully custom **feedforward neural network** built from scratch using only NumPy, trained to classify handwritten digits (0–9) from the [Kaggle Digit Recognizer](https://www.kaggle.com/c/digit-recognizer) dataset. No deep learning frameworks — every layer, activation, loss, and optimizer is implemented manually.

---

## 📁 Project Structure

```
├── FINAL_PROJECT_WITH_SGD_only.ipynb   # Full pipeline: preprocessing → training → evaluation
```

---

## 🧠 Model Architecture

The network is a configurable multi-layer perceptron (MLP):

```
Input Layer    →   784 neurons  (28×28 flattened pixels)
Hidden Layer 1 →   256 neurons  (ReLU)
Hidden Layer 2 →   128 neurons  (ReLU)
Output Layer   →    10 neurons  (Softmax → digits 0–9)
```

All weights are initialized using **Xavier/Glorot initialization** to ensure stable gradient flow.

---

## ⚙️ Pipeline Overview

### 1. Data Preprocessing
- Loads the Kaggle `train.csv` dataset
- Normalizes pixel values to `[0, 1]` by dividing by 255
- One-hot encodes labels using `sklearn`'s `OneHotEncoder`
- Handles missing values via `SimpleImputer`

### 2. Data Splitting
| Split      | Size |
|------------|------|
| Train      | 60%  |
| Validation | 20%  |
| Test       | 20%  |

### 3. Activation Functions
All implemented manually:

| Function | Used In       |
|----------|---------------|
| ReLU     | Hidden layers |
| Softmax  | Output layer  |
| Sigmoid  | Available     |
| Tanh     | Available     |
| Linear   | Available     |

### 4. Loss Function
**Categorical Cross-Entropy** with numerical stability (`log(ŷ + 1e-8)`):

```
L = - (1/m) * Σ y * log(ŷ)
```

### 5. Optimizer — SGD with Mini-Batches
- **Batch size:** 32
- Shuffles training data each epoch
- Updates weights via standard gradient descent:
  ```
  W = W - lr * dW
  b = b - lr * db
  ```

### 6. Training Features
- **Early stopping** with configurable patience
- Saves the best weights based on validation loss
- Logs training and validation loss every 100 epochs
- Plots loss curves after training

### 7. Evaluation
- Accuracy score on train, validation, and test sets
- Full **confusion matrix** (10×10) using `pandas.crosstab`

---

## 🚀 Getting Started

### Prerequisites

```bash
pip install numpy pandas matplotlib scikit-learn
```

### Dataset

Download the dataset from Kaggle:
[https://www.kaggle.com/c/digit-recognizer/data](https://www.kaggle.com/c/digit-recognizer/data)

Place `train.csv` in your working directory and update the path in the notebook:

```python
data = pd.read_csv("train.csv")
```

### Run

Open and run the notebook cell by cell:

```bash
jupyter notebook FINAL_PROJECT_WITH_SGD_only.ipynb
```

---

## 📊 Sample Output

```
Epoch 0:   Train Loss: 2.3012, Val Loss: 2.3008
Epoch 100: Train Loss: 0.4821, Val Loss: 0.5103
Epoch 200: Train Loss: 0.3015, Val Loss: 0.3412
Early stopping at epoch 340. Best val loss: 0.3187

Training Set Evaluation:
Accuracy: 0.9412

Validation Set Evaluation:
Accuracy: 0.9178

Test Set Evaluation:
Accuracy: 0.9154
```

---

## 🔑 Key Implementation Details

- **No PyTorch / TensorFlow** — pure NumPy matrix operations throughout
- **Backpropagation** implemented manually layer by layer using the chain rule
- **Modular design** — `NeuralNetworkSgd` is the base class; `digitClassifier` extends it with training logic
- **Configurable** — layer sizes and activations are passed as lists, so the architecture is easy to modify

```python
layer_sizes = [784, 256, 128, 10]
activations  = ['relu', 'relu', 'softmax']
model = digitClassifier(layer_sizes, activations)
```

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
