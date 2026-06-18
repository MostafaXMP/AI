# 🧬 Genetic Algorithm — Knapsack Problem & Pattern Optimization

This repository contains two Python implementations of a **Genetic Algorithm (GA)**: one applied to the classic **0/1 Knapsack Problem**, and one demonstrating the core GA mechanics on binary string optimization.

---

## 📁 Project Structure

```
├── Genetic_Algorithm_Knapsack.ipynb   # GA solution for the 0/1 Knapsack Problem
└── Genetic_Algorithm.py               # GA applied to binary string pattern matching
```

---

## 📌 Overview

### 1. Knapsack Problem (`Genetic_Algorithm_Knapsack.ipynb`)

Solves the **0/1 Knapsack Problem** using a Genetic Algorithm. Given a set of items with weights and values, the algorithm finds the optimal subset that maximizes total value without exceeding a weight limit.

**Items used:**

| Item | Weight | Value |
|------|--------|-------|
| 1    | 1      | 2     |
| 2    | 2      | 4     |
| 3    | 3      | 4     |
| 4    | 4      | 5     |
| 5    | 5      | 7     |
| 6    | 6      | 9     |

**Parameters:**

| Parameter            | Value |
|----------------------|-------|
| Max Weight           | 10    |
| Population Size      | 10    |
| Mutation Probability | 0.2   |
| Generations          | 10    |

---

### 2. Binary String Optimizer (`Genetic_Algorithm.py`)

A foundational GA that evolves a population of 9-bit binary strings to maximize the occurrence of the pattern `"010"` within each chromosome. Runs for 2 iterations and clearly prints each step of the GA process.

---

## 🔬 How the Genetic Algorithm Works

Both implementations follow the standard GA pipeline:

```
1. Initialization   →  Generate a random population of individuals (chromosomes)
2. Evaluation       →  Compute the fitness of each individual
3. Selection        →  Select the fittest individuals as parents (tournament / ranking)
4. Crossover        →  Combine parents to produce offspring (single-point crossover)
5. Mutation         →  Randomly flip bits to maintain diversity
6. Replacement      →  Form the next generation and repeat
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- Jupyter Notebook (for the `.ipynb` file)

### Installation

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### Run the Knapsack Notebook

```bash
jupyter notebook Genetic_Algorithm_Knapsack.ipynb
```

### Run the Binary String Optimizer

```bash
python Genetic_Algorithm.py
```

---

## 📊 Sample Output — Knapsack

```
generation 1:
best chromosome: [1, 1, 0, 0, 0, 1]
fitness (Total Value): 15
---------------------------------------------------
...
Final Solution:
Best Chromosome: [1, 1, 1, 1, 0, 0]
total value: 15
```

Each `1` in the chromosome means the corresponding item is included in the knapsack.

---

## 🧠 Key Concepts

- **Chromosome**: A binary list representing which items are selected (Knapsack) or a binary string (optimizer).
- **Fitness Function**: Returns the total value of selected items if within weight limit; returns `0` for overweight solutions.
- **Tournament Selection**: Randomly picks 3 candidates and selects the best as a parent.
- **Single-Point Crossover**: Splits two parents at a random point and swaps their tails.
- **Mutation**: Each bit has a probability of being flipped to encourage exploration.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
