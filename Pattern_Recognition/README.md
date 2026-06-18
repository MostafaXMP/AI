# cat-dog-classifier

A classical machine learning pipeline for **binary image classification** — cats vs. dogs — built without deep learning. Six traditional classifiers are trained on raw pixel features extracted from the [Microsoft Cats vs. Dogs dataset](https://www.microsoft.com/en-us/download/details.aspx?id=54765), compared head-to-head, and the best-performing model is used to predict new user-supplied images.

---

## Dataset

**PetImages** — 1,500 images sampled per class (3,000 total) from the Cats vs. Dogs dataset.

| Property | Detail |
|----------|--------|
| Source | Microsoft / Kaggle Cats vs. Dogs |
| Classes | Cat (0), Dog (1) |
| Images per class | 1,500 (randomly sampled) |
| Image format | Resized to 64×64, converted to grayscale |
| Feature vector | 4,096 raw pixel values, normalised to [0, 1] |

---

## Pipeline

```
Raw Images (Cat / Dog)
    └── Load & validate (skip corrupt files)
            └── Resize to 64×64 → Grayscale → Flatten → Normalise [0,1]
                    └── Feature Selection: SelectKBest (top 2,000 / 4,096 features)
                            └── Data Augmentation (Gaussian noise perturbation → 2× dataset)
                                    └── Train/Test Split (75% / 25%, stratified)
                                            └── Train & Evaluate 6 Classifiers
                                                    └── Best Model → Image Predictor
```

---

## Feature Engineering

Since no CNN is used, two steps reduce noise and dimensionality before training:

**Feature Selection** — `SelectKBest` with ANOVA F-scores selects the 2,000 most discriminative pixels out of 4,096, cutting dimensionality by ~51%.

**Data Augmentation** — each image is duplicated with small Gaussian noise (σ = 0.05) added to pixel values, doubling the training set and reducing overfitting on the flat feature representation.

---

## Models Compared

| Model | Key Hyperparameters |
|-------|-------------------|
| Random Forest | 100 trees, max depth 10, min samples split 20 |
| K-Nearest Neighbours | k=5, distance-weighted |
| SVM | RBF kernel, C=1.0 |
| Logistic Regression | C=1.0, max iter 200 |
| Decision Tree | max depth 8, min samples split 15 |
| Naive Bayes | Gaussian |

Each model is evaluated on: test accuracy, training accuracy (overfitting check), confusion matrix, full classification report (precision / recall / F1), and training + inference time.

---

## Evaluation & Visualisation

- **Grouped bar chart** — training vs. test accuracy for all 6 models side by side
- **Confusion matrices** — seaborn heatmaps per model
- **Best model selection** — automatically chosen by highest test accuracy and used for the image predictor

---

## Image Predictor

After training, the best model can classify any new image:

1. Loads and preprocesses the image (resize → grayscale → flatten → normalise)
2. Applies the same `SelectKBest` selector fitted during training
3. Outputs the predicted class (Cat / Dog) and confidence score (if the model supports `predict_proba`)
4. Displays the image with the prediction as the title

---

## Project Structure

```
cat-dog-classifier/
│
├── Patter_Final_Project.ipynb   # Full pipeline: loading, training, evaluation, predictor
├── PetImages/
│   ├── Cat/                     # ~12,500 cat images (1,500 used)
│   └── Dog/                     # ~12,500 dog images (1,500 used)
└── README.md
```

---

## Requirements

- Python 3.7+
- NumPy, Pandas
- OpenCV (`opencv-python`)
- scikit-learn
- Matplotlib, Seaborn

Install dependencies:

```bash
pip install numpy pandas opencv-python scikit-learn matplotlib seaborn
```

---

## Usage

1. Download the [Cats vs. Dogs dataset](https://www.microsoft.com/en-us/download/details.aspx?id=54765) and extract it so `PetImages/Cat/` and `PetImages/Dog/` exist.
2. Update `folder_path` in the Data Loading cell to your local path.
3. To predict a new image, update `user_image_path` in the Image Predictor cell.
4. Run the notebook:

```bash
jupyter notebook Patter_Final_Project.ipynb
```

---

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Flat pixel features** | Treating each pixel value as an independent feature — simple but ignores spatial structure |
| **SelectKBest (ANOVA F)** | Ranks features by how well they separate the two classes statistically; keeps the top k |
| **Gaussian noise augmentation** | Creates synthetic variants of each sample by adding small random perturbations |
| **Stratified split** | Ensures the same Cat/Dog ratio is preserved in both train and test sets |
| **Overfitting check** | Comparing train vs. test accuracy — a large gap signals the model memorised rather than generalised |
| **RBF SVM** | Maps data into a high-dimensional space where a linear boundary can separate non-linearly separable classes |
