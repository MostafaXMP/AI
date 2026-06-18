# gridworld-mdp-solver

A Python implementation of classic Markov Decision Process (MDP) planning algorithms applied to a 4×4 GridWorld environment. This project demonstrates and compares **Value Iteration** and **Policy Iteration** under different discount factors.

---

## Problem Description

The environment is a **4×4 GridWorld** where an agent navigates from any starting cell toward a goal while avoiding a pit.

| Element | Position | Reward |
|---------|----------|--------|
| Goal | (3, 3) | +10 |
| Pit | (2, 2) | −10 |
| Every other step | — | −1 |

The agent can move in four directions: **Up (U), Down (D), Left (L), Right (R)**. Movements that would go out of bounds leave the agent in place. The goal and pit are terminal states.

---

## Algorithms

### Value Iteration
Iteratively updates the value of each state using the Bellman optimality equation until convergence (change < θ = 0.001):

```
V(s) ← max_a [ R(s, a) + γ · V(s') ]
```

### Policy Iteration
Alternates between two steps until the policy stabilises:

1. **Policy Evaluation** — computes V under the current policy until convergence.
2. **Policy Improvement** — updates the policy greedily with respect to V.

---

## Results

Experiments are run for two discount factors: **γ = 0.0** and **γ = 0.9**.

### γ = 0.0 (myopic agent)
The agent only cares about the immediate next reward, so values reflect one-step lookahead only.

```
Value Function:
[[-1. -1. -1. -1.]
 [-1. -1. -1. -1.]
 [-1. -1.  0. 10.]
 [-1. -1. 10.  0.]]
```

### γ = 0.9 (far-sighted agent)
The agent accounts for future rewards, producing a smooth value gradient across the grid.

```
Value Function:
[[ 1.81  3.12  4.58  6.2 ]
 [ 3.12  4.58  6.2   8.  ]
 [ 4.58  6.2   0.   10.  ]
 [ 6.2   8.   10.    0.  ]]

Optimal Policy:
['D', 'D', 'D', 'D']
['D', 'D', 'R', 'D']
['D', 'D', 'T', 'D']
['R', 'R', 'R', 'T']
```
*(T = Terminal state)*

Both algorithms converge to the same value function and optimal policy, confirming their theoretical equivalence.

---

## Project Structure

```
gridworld-mdp-solver/
│
├── MDP_Assignment_1.ipynb   # Main notebook with implementation and results
└── README.md
```

---

## Requirements

- Python 3.7+
- NumPy

Install dependencies:

```bash
pip install numpy
```

---

## Usage

Open and run the notebook:

```bash
jupyter notebook MDP_Assignment_1.ipynb
```

The notebook will print the Value Iteration and Policy Iteration value functions and the derived policy for each discount factor.

---

## Key Concepts

- **MDP (Markov Decision Process)** — a framework for sequential decision-making under uncertainty.
- **Discount Factor (γ)** — controls how much the agent values future rewards relative to immediate ones. γ = 0 is fully myopic; γ → 1 is fully far-sighted.
- **Convergence threshold (θ)** — iterations stop when the maximum change in any state value falls below 0.001.
