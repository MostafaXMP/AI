# 📈 StudentScore-LR: Student Performance Predictor

A machine learning project that predicts student academic performance using **Multiple Linear Regression**, built with a full ML pipeline — from EDA to evaluation. Includes a comparison between scikit-learn's `LinearRegression` and `statsmodels OLS`.

---

## 📌 Overview

This project explores what factors most influence a student's Performance Index using the [Student Performance Dataset](https://www.kaggle.com/datasets/nikhil7280/student-performance-multiple-linear-regression) from Kaggle. It follows a complete, structured ML workflow and serves as a practical demonstration of regression fundamentals.

**Target variable:** `Performance Index` (continuous)

**Features used:**
| Feature | Type |
|---|---|
| Hours Studied | Numerical |
| Previous Scores | Numerical |
| Sleep Hours | Numerical |
| Sample Question Papers Practiced | Numerical |
| Extracurricular Activities | Categorical (Yes/No → encoded) |

---

## 🗂️ Project Structure

```
├── Practice.ipynb          # Main notebook with full ML pipeline
└── Student_Performance.csv # Dataset (download from Kaggle)
```

---

## 🔬 Workflow

### 1. Exploratory Data Analysis (EDA)
- Shape, data types, and descriptive statistics
- Distribution plot of the target variable (`Performance Index`)
- Pairplot for feature relationships
- Correlation heatmap (numeric features only)
- Boxplot for outlier inspection

### 2. Data Cleaning
- No missing values found
- Duplicates identified and retained (minimal impact)
- No outliers requiring removal

### 3. Feature Engineering
- `Extracurricular Activities` (Yes/No) encoded using `OrdinalEncoder`
- No scaling required (linear regression is scale-invariant for this dataset)

### 4. Modeling

**Model A — scikit-learn LinearRegression**
- Standard `train_test_split` (80/20)
- Scatter plots comparing predictions vs. actuals per feature

**Model B — statsmodels OLS**
- Full statistical summary including p-values, confidence intervals, and R²
- Useful for understanding feature significance

**Model C — OLS vs Ridge (bias-variance demo)**
- Visual comparison of OLS and Ridge regression under data perturbation
- Illustrates the underfitting/overfitting trade-off

### 5. Evaluation Metrics

| Metric | Description |
|---|---|
| MAE | Mean Absolute Error |
| MSE | Mean Squared Error |
| RMSE | Root Mean Squared Error |
| R² | Coefficient of Determination |
| Adjusted R² | R² penalized for number of features |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/StudentScore-LR.git
cd StudentScore-LR
```

### 2. Install dependencies

```bash
pip install pandas numpy matplotlib seaborn scikit-learn statsmodels
```

### 3. Download the dataset

Get `Student_Performance.csv` from [Kaggle](https://www.kaggle.com/datasets/nikhil7280/student-performance-multiple-linear-regression) and place it in the project root.

### 4. Run the notebook

```bash
jupyter notebook Practice.ipynb
```

---

## 💡 Key Findings

- `Previous Scores` and `Hours Studied` are the strongest predictors of performance
- Students with 4 study hours, extracurricular activities, and high practice paper scores tend to achieve a Performance Index ≥ 85
- Both sklearn and statsmodels produce identical predictions — statsmodels adds interpretability through its full OLS summary
- The Ridge vs OLS demo visually shows how regularization reduces variance under noisy data

---

## 🛠️ Requirements

- Python 3.8+
- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- statsmodels

---

## 🚧 Planned Improvements

- Implement Linear Regression from scratch using gradient descent (NumPy only)
- Add polynomial regression for non-linear feature relationships
- Add cross-validation instead of a single train/test split
- Build a simple prediction interface (e.g., Streamlit app)

---

## 📄 License

This project is for educational purposes. Dataset sourced from Kaggle under its respective license.
