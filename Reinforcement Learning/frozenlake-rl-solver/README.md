# frozenlake-rl-solver

A Python implementation of two **model-free reinforcement learning** algorithms — **Monte Carlo Policy Control** and **SARSA** — applied to the classic FrozenLake-v1 environment from Gymnasium. Both algorithms learn an optimal policy purely from interaction with the environment, without access to a transition model.

---

## Environment

**FrozenLake-v1** (deterministic, `is_slippery=False`) from [Gymnasium](https://gymnasium.farama.org/environments/toy_text/frozen_lake/).

The agent navigates a 4×4 frozen lake grid from the top-left corner (Start) to the bottom-right corner (Goal), avoiding holes.

```
S  F  F  F
F  H  F  H
F  F  F  H
H  F  F  G
```

| Cell | Meaning | Reward |
|------|---------|--------|
| S | Start | 0 |
| F | Frozen (safe) | 0 |
| H | Hole (terminal) | 0 |
| G | Goal (terminal) | +1 |

- **States:** 16 (one per grid cell)
- **Actions:** 4 — Left (←), Down (↓), Right (→), Up (↑)
- **Episodes end** when the agent falls in a hole or reaches the goal.

---

## Algorithms

### Monte Carlo Policy Control (First-Visit)
An episodic, model-free method that learns Q-values by averaging the **actual returns** observed after each first visit to a (state, action) pair across full episodes.

- Exploration via **ε-greedy** policy (ε = 0.2)
- Updates happen **after** each complete episode
- Uses a running average: `Q(s,a) ← mean of all observed returns`

### SARSA (On-Policy TD Control)
A temporal-difference method that updates Q-values **online** after every step, using the next action actually taken by the current policy.

Update rule:
```
Q(s, a) ← Q(s, a) + α · [r + γ · Q(s', a') − Q(s, a)]
```

- Exploration via **ε-greedy** policy (ε = 0.2)
- Learning rate α = 0.1, discount factor γ = 0.99
- Updates happen **at every step** (no need to wait for episode end)

---

## Results

Both algorithms were trained for **10,000 episodes** and evaluated greedily over **1,000 episodes**.

### Monte Carlo Policy
```
↓ ← ↑ ←
↓ T ↓ T
→ ↓ ↓ T
T → → T
```
**Success Rate: 100.00%**

### SARSA Policy
```
↓ ← ← ←
↓ T ↑ T
→ → ↓ T
T → → T
```
**Success Rate: 100.00%**

*(T = Terminal state — Hole or Goal)*

Both algorithms converge to a policy that successfully navigates to the goal every time in the deterministic environment.

---

## Project Structure

```
frozenlake-rl-solver/
│
├── Assignment_2.ipynb   # Main notebook with implementation and results
└── README.md
```

---

## Requirements

- Python 3.7+
- NumPy
- Gymnasium

Install dependencies:

```bash
pip install numpy gymnasium
```

---

## Usage

Open and run the notebook:

```bash
jupyter notebook Assignment_2.ipynb
```

The notebook will train both algorithms, print the learned policy grid, and report the greedy evaluation success rate for each.

---

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Model-free RL** | Learns from experience without knowing the environment's transition probabilities |
| **On-policy** | Both MC and SARSA improve the same policy used for exploration |
| **ε-greedy exploration** | With probability ε, a random action is taken; otherwise the best-known action is chosen |
| **First-Visit MC** | Only the first occurrence of each (s, a) pair per episode contributes to the return average |
| **TD learning (SARSA)** | Bootstraps from the next step's Q-value instead of waiting for the full episode return |
| **Discount factor (γ = 0.99)** | Agent is nearly fully far-sighted, valuing future rewards almost as much as immediate ones |
