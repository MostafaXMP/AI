# foodmart-store-clustering

A data mining project that analyses **150 FOODmart retail stores** across 8 Australian states, applying five clustering techniques to segment stores by customer behaviour and operational profile, then training a classifier to predict cluster membership on unseen data.

---

## Dataset

`StoresData.xlsx` — 150 rows, one per store, with features covering:

| Category | Features |
|----------|----------|
| Financial | Gross Profit, Advertisement Spend, Basket size (2013 & 2014) |
| Operational | Hours Trading, Car Spaces, Competitors count |
| Workforce | Union %, Manager Experience, Manager Training |
| Encoded categoricals | Location, State, Sundays trading, Home Delivery |

Columns irrelevant to customer behaviour (Sales $m, Wages $m, No. Staff, Manager Age/Sex, raw categorical strings) are dropped before analysis.

---

## Pipeline

```
Raw Data
    └── Cleaning (nulls, duplicates)
            └── Outlier Removal (IQR method, per numerical column)
                    └── Standard Scaling
                            ├── Clustering (5 techniques)
                            ├── Silhouette Evaluation
                            ├── Visualisation (KDE, PCA scatter, Pie charts)
                            └── Classification (Random Forest on K-Means labels)
```

---

## Clustering Techniques

Five algorithms were applied and compared. Only the first two were deemed successful based on silhouette scores and visual separation.

### Successful

| Method | Config | Notes |
|--------|--------|-------|
| **K-Means** | k=3, selected via Elbow Method | Best separation; used as ground truth for classification |
| **Hierarchical** | Complete linkage, Euclidean, cut at 3 clusters | Dendrogram clearly shows 3-cluster structure at height 9–10 |

### Unsuccessful (poor silhouette scores / visible overlap)

| Method | Config | Issue |
|--------|--------|-------|
| K-Medoids | k=3, Manhattan distance, heuristic init | Cluster overlap |
| DBSCAN | eps=2.9, min_samples=5 | High outlier count |
| HDBSCAN | min_cluster_size=2 | Similar to DBSCAN; many noise points |

---

## Cluster Profiles (K-Means, k=3)

| Feature | Cluster 0 | Cluster 1 | Cluster 2 |
|---------|-----------|-----------|-----------|
| Gross Profit | Highest | Lowest | Moderate |
| Ad Spend | Highest | Moderate | Moderate |
| Competitors | Lowest | Highest | Moderate |
| Car Spaces | Highest | Moderate | Moderate |
| Hours Trading | Lowest | Highest | Moderate |
| Union % | Moderate | Moderate | Highest |
| Manager Experience | Moderate | Highest | Moderate |
| Basket 2013/2014 | Highest | Moderate | Lowest |

**Cluster 0** — High-performing stores: strong profits and basket sizes, low competition, heavy advertising.  
**Cluster 1** — Struggling stores: experienced managers, long hours, but squeezed by high competition.  
**Cluster 2** — Low performers: high union presence, low basket values across both years.

---

## Visualisation

Three plot types are produced for all five clustering methods side by side:

- **KDE pair plots** — per-feature density distributions coloured by K-Means cluster
- **PCA scatter plots** — 2D projection of all methods for visual separation comparison
- **Pie charts** — cluster size proportions per method

---

## Classification

K-Means cluster labels are used as the target variable to train a supervised classifier:

| Step | Detail |
|------|--------|
| Features | All scaled numerical columns |
| Target | K-Means cluster label (0, 1, or 2) |
| Split | 80% train / 20% test |
| Model | Random Forest Classifier (default hyperparameters) |
| Evaluation | Classification report (precision, recall, F1) + Confusion matrix |

---

## Project Structure

```
foodmart-store-clustering/
│
├── v6DataMiningSnapshot.ipynb   # Full pipeline: preprocessing → clustering → classification
├── StoresData.xlsx              # Input dataset (150 stores)
└── README.md
```

---

## Requirements

- Python 3.7+
- pandas, numpy
- scikit-learn
- scikit-learn-extra (for K-Medoids)
- hdbscan
- scipy
- matplotlib, seaborn

Install dependencies:

```bash
pip install pandas numpy scikit-learn scikit-learn-extra hdbscan scipy matplotlib seaborn openpyxl
```

> **Note:** The notebook pins `numpy==1.23.5` for compatibility with `hdbscan`. If you encounter version conflicts, run `pip install numpy==1.23.5` first.

---

## Usage

1. Place `StoresData.xlsx` in `/content/sample_data/` (Google Colab default) or update the path in the loading cell.
2. Open and run the notebook:

```bash
jupyter notebook v6DataMiningSnapshot.ipynb
```

---

## Key Concepts

| Concept | Description |
|---------|-------------|
| **IQR outlier removal** | Removes points beyond 1.5× the interquartile range from each feature independently |
| **Standard scaling** | Centres each feature to mean=0, std=1 so no single feature dominates distance-based algorithms |
| **Elbow method** | Plots WCSS vs k to find where adding more clusters yields diminishing returns |
| **Silhouette score** | Measures how similar a point is to its own cluster vs the nearest other cluster; ranges from −1 to 1 |
| **PCA** | Reduces high-dimensional data to 2 components for visual inspection of cluster separation |
| **Complete linkage** | Hierarchical clustering variant that merges clusters based on maximum pairwise distance |
| **Random Forest** | Ensemble of decision trees; used here to learn the cluster boundaries found by K-Means |
