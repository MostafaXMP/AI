# KNNLoanClassifier — K-Nearest Neighbours with Cross-Validation on Loan Data

A machine learning assignment notebook that applies **K-Nearest Neighbours (KNN)** classification to predict loan approval status, with a focus on hyperparameter tuning, k-fold cross-validation, and overfitting analysis.

---

## Overview

This project builds on a loan dataset to explore how KNN performs as a binary classifier, how to select the optimal K value, and whether cross-validation produces a more robust performance estimate than a single validation split.

| Aspect | Detail |
|---|---|
| Algorithm | K-Nearest Neighbours (KNN) |
| Dataset | `loan_data.csv` |
| Task | Binary classification — loan approved or not |
| Key focus | K tuning, GridSearchCV, k-fold cross-validation, overfitting |

---

## Dataset

**`loan_data.csv`** — Loan applicant records with financial and personal attributes.

**Features used (after selection):**

| Feature | Type | Preprocessing |
|---|---|---|
| person_home_ownership | Categorical | OneHotEncoded |
| previous_loan_defaults_on_file | Categorical | OneHotEncoded |
| loan_amnt, loan_int_rate, etc. | Numeric | MinMaxScaled |

**Dropped features:** `loan_status` (target), `person_gender`, `person_education`, `person_emp_exp`, `cb_person_cred_hist_length`, `person_age`, `loan_intent`

**Target:** `loan_status` — binary (approved / not approved)

---

## Project Structure

```
KNNLoanClassifier/
│
├── MachineLearningAssignment2__2_.ipynb   # Main notebook
├── loan_data.csv                          # Dataset
└── README.md
```

---

## Workflow

### 1. Data Import & Preprocessing
- Null and duplicate checks
- Feature selection (dropped low-correlation and non-numeric columns)
- MinMaxScaler on numeric columns
- OneHotEncoder on categorical columns via ColumnTransformer

### 2. Data Splitting
Three-way split to enable proper validation:

```
Full dataset
├── 80% → Training + Validation
│   ├── 60% → Training set   (X_train)
│   └── 20% → Validation set (X_val)
└── 20% → Test set           (X_test)
```

### 3. KNN — Finding Optimal K
- Trained KNN models for K = 1 to 20
- Evaluated each on the validation set using Accuracy, Precision, Recall, and F1
- Plotted validation scores across K values to visually identify the elbow
- **Optimal K selected: 11**

### 4. Cross-Validation
- 5-fold cross-validation applied to the training set using `GridSearchCV`
- Parameters tuned: `n_neighbors=11`, `weights=uniform`, `p=1` (Manhattan distance), `algorithm=brute`, `leaf_size=2`
- Cross-val mean accuracy compared against validation and test set accuracy
- **Finding:** Cross-validation scores closely matched validation and test accuracy, confirming it is a reliable estimator

### 5. Evaluation
- Confusion matrix (heatmap) on test set
- Full classification report (precision, recall, F1, support) on both train and test sets
- **Observation:** Both models predict more false negatives than false positives

### 6. Overfitting Analysis & Improvement
- Training accuracy > test accuracy → overfitting detected
- Mitigation attempted by increasing K to 17 (higher K = smoother decision boundary = less overfitting)
- Classification reports compared before and after the adjustment

---

## Evaluation Metrics

The custom `evaluate_preds()` helper reports four metrics for every prediction:

| Metric | Description |
|---|---|
| Accuracy | Proportion of correct predictions |
| Precision | Of predicted positives, how many are truly positive |
| Recall | Of actual positives, how many were correctly identified |
| F1 Score | Harmonic mean of precision and recall |

---

## Requirements

```
numpy
pandas
matplotlib
scikit-learn
```

Install all dependencies with:

```bash
pip install numpy pandas matplotlib scikit-learn
```

---

## Usage

1. Place `loan_data.csv` in the same directory as the notebook (or update the path in the `read_csv` call).
2. Open the notebook:
   ```bash
   jupyter notebook MachineLearningAssignment2__2_.ipynb
   ```
3. Run all cells top to bottom. The notebook is structured in sequential stages — preprocessing → splitting → KNN tuning → cross-validation → evaluation → overfitting analysis.

---

## Key Concepts Demonstrated

- K-Nearest Neighbours for binary classification
- Manual hyperparameter search (K = 1–20) with validation set
- GridSearchCV with 5-fold cross-validation
- Three-way train/validation/test split
- Overfitting detection and mitigation via K tuning
- Confusion matrix and full classification report analysis
- Comparing cross-validation reliability against held-out sets
