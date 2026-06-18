# RegressionLab — Linear & Logistic Regression on Insurance and Loan Datasets

A machine learning assignment notebook that explores and compares **regression techniques** across two real-world datasets: medical insurance charges (regression) and loan approval status (classification).

---

## Overview

The notebook is divided into two major parts:

| Part | Algorithm | Dataset | Task |
|---|---|---|---|
| Part 1 | Linear Regression (Simple, Multiple, Polynomial) | `insurance.csv` | Predict medical charges |
| Part 2 | Logistic Regression | `loan_data.csv` | Predict loan approval status |

---

## Datasets

### `insurance.csv`
Medical insurance cost data used for continuous value prediction.

| Feature | Description |
|---|---|
| age | Age of the individual |
| sex | Gender (label encoded) |
| bmi | Body Mass Index |
| children | Number of dependants |
| smoker | Smoking status (label encoded) |
| region | Residential region (label encoded) |
| **charges** | **Target — medical insurance cost** |

### `loan_data.csv`
Loan applicant data used for binary classification.

Selected features (others dropped as less correlated):

| Feature | Description |
|---|---|
| person_home_ownership | Home ownership type (one-hot encoded) |
| previous_loan_defaults_on_file | Prior default history (one-hot encoded) |
| loan_amnt, loan_int_rate, etc. | Numeric loan attributes (MinMax scaled) |
| **loan_status** | **Target — loan approved (1) or not (0)** |

---

## Project Structure

```
RegressionLab/
│
├── 1781639012440_MLAssignment.ipynb   # Main notebook
├── insurance.csv                      # Dataset for linear regression
├── loan_data.csv                      # Dataset for logistic regression
└── README.md
```

---

## Workflow

### Part 1 — Linear Regression (Insurance Dataset)

#### Data Exploration & Preprocessing
- Null and duplicate checks
- Label encoding of categorical columns (`sex`, `smoker`, `region`)
- Correlation heatmap and pairplot (age, BMI, smoker, charges)
- 80/20 train-test split; StandardScaler applied to features

#### Models

**Simple Linear Regression**
- Single feature: `smoker` (highest correlation with charges)
- Plots regression line over scatter of smoker vs. charges

**Multiple Linear Regression**
- All features used with StandardScaler
- Predicted vs. Actual scatter plot with regression line

**Polynomial Regression**
- Feature: `age` (second most correlated; chosen over `smoker` which is binary)
- Degrees tested: 2, 3, 4
- R² and MSE reported per degree; regression curve plotted for each

#### Summary (from notebook)
> Multiple Linear Regression (all features) was the most effective predictor. Polynomial Regression on `age` performed worst — increasing degree did not improve the model.

---

### Part 2 — Logistic Regression (Loan Dataset)

#### Data Exploration & Preprocessing
- Duplicate check
- Feature selection: dropped `loan_status`, `person_gender`, `person_education`, `person_emp_exp`, `cb_person_cred_hist_length`, `person_age`, `loan_intent`
- MinMaxScaler on numeric columns
- OneHotEncoder on `person_home_ownership` and `previous_loan_defaults_on_file` via ColumnTransformer

#### Model
- 80/20 train-test split
- Logistic Regression trained and scored
- Confusion matrix plotted as a seaborn heatmap
- Accuracy score reported

---

## Requirements

```
numpy
pandas
matplotlib
seaborn
scikit-learn
```

Install all dependencies with:

```bash
pip install numpy pandas matplotlib seaborn scikit-learn
```

---

## Usage

1. Place `insurance.csv` and `loan_data.csv` in the same directory as the notebook.
2. Open the notebook:
   ```bash
   jupyter notebook 1781639012440_MLAssignment.ipynb
   ```
3. Run all cells top to bottom. The two parts (Linear Regression and Logistic Regression) are independent — each has its own imports and preprocessing section.

---

## Key Concepts Demonstrated

- Simple, Multiple, and Polynomial Linear Regression
- Feature correlation analysis with heatmaps
- Encoding strategies: LabelEncoder vs. OneHotEncoder
- Feature scaling: StandardScaler vs. MinMaxScaler
- Binary classification with Logistic Regression
- Model evaluation: R², MSE (regression) and Accuracy, Confusion Matrix (classification)
