# cartpole-a2c

A PyTorch implementation of the **Advantage Actor-Critic (A2C)** algorithm applied to the classic **CartPole-v1** control task from Gymnasium. The agent learns to balance a pole on a moving cart using two separate neural networks — an Actor that selects actions and a Critic that evaluates them.

---

## Environment

**CartPole-v1** from [Gymnasium](https://gymnasium.farama.org/environments/classic_control/cart_pole/).

The agent controls a cart on a frictionless track and must keep a pole balanced upright by pushing left or right. An episode ends when the pole falls past ±12°, the cart moves out of bounds, or 500 steps are reached.

| Property | Detail |
|----------|--------|
| State space | 4 continuous values (cart position, cart velocity, pole angle, pole angular velocity) |
| Action space | 2 discrete actions (push left, push right) |
| Max reward | 500 (one point per timestep survived) |
| Goal | Average reward ≥ 475 over 100 consecutive episodes |

---

## Algorithm: Advantage Actor-Critic (A2C)

A2C is a **policy gradient** method that uses two networks trained simultaneously:

- **Actor** — a policy network π(a|s) that outputs action probabilities. Trained to maximise expected advantage.
- **Critic** — a value network V(s) that estimates the expected return from each state. Trained to minimise MSE against the actual discounted returns.

The key quantity is the **Advantage**:

```
A(s, a) = G_t − V(s)
```

where G_t is the discounted return from step t. A positive advantage means the action did better than expected; a negative one means it did worse. This signal reduces variance compared to vanilla policy gradient while keeping the update unbiased.

### Update Rules

**Actor loss** (minimise negative expected advantage):
```
L_actor = −E[ log π(a|s) · A(s, a) ]
```

**Critic loss** (fit value function to returns):
```
L_critic = MSE( V(s), G_t )
```

Advantages are normalised per episode for training stability.

---

## Network Architecture

Both networks share the same structure but different output heads:

```
Input (state_dim=4)
    └── Linear(4 → 128) + ReLU
            └── Actor: Linear(128 → 2) + Softmax   → action probabilities
            └── Critic: Linear(128 → 1)             → state value V(s)
```

---

## Hyperparameters

| Parameter | Value |
|-----------|-------|
| Discount factor (γ) | 0.99 |
| Actor learning rate | 1e-3 |
| Critic learning rate | 1e-3 |
| Training episodes | 600 |
| Evaluation episodes | 5 |
| Optimiser | Adam |
| Random seed | 42 |

---

## Project Structure

```
cartpole-a2c/
│
├── RL_Assignment3.ipynb   # Main notebook: model, training loop, evaluation, plot
└── README.md
```

---

## Requirements

- Python 3.7+
- PyTorch
- Gymnasium
- NumPy
- Matplotlib

Install dependencies:

```bash
pip install torch gymnasium numpy matplotlib
```

---

## Usage

Open and run the notebook:

```bash
jupyter notebook RL_Assignment3.ipynb
```

The notebook will:
1. Train the A2C agent for 600 episodes, printing average reward every 20 episodes.
2. Plot the training reward curve.
3. Run a greedy evaluation over 5 episodes and print per-episode and average rewards.

---

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Policy gradient** | Directly optimises the policy by following the gradient of expected return |
| **Actor-Critic** | Combines a policy network (actor) with a value-estimating baseline (critic) to reduce gradient variance |
| **Advantage** | Measures how much better an action was than the average action in that state — centres the learning signal |
| **Discounted return G_t** | Weighted sum of future rewards: r_t + γr_{t+1} + γ²r_{t+2} + … |
| **Advantage normalisation** | Standardising advantages per episode improves gradient stability |
| **On-policy learning** | A2C uses data collected under the current policy; the policy must be updated after each episode |
