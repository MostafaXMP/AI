# graph-search-algorithms

A Python implementation of three classic **uninformed graph search algorithms** — BFS, DFS, and UCS — each applied to the same sample graph to find a path from a start node to a goal node. Written from scratch using only Python built-ins, with detailed inline comments explaining every step.

---

## Algorithms

### BFS — Breadth-First Search (`BFS.py`)
Explores nodes level by level, always expanding the shallowest unvisited node first. Uses a **queue** (FIFO) to track paths.

- Guaranteed to find the **shortest path** in terms of number of edges
- Explores broadly before going deep

### DFS — Depth-First Search (`DFS.py`)
Explores as far as possible along each branch before backtracking. Uses a **stack** (LIFO) to track paths.

- Does **not** guarantee the shortest path
- Uses less memory than BFS on wide graphs

> **Note:** The function in `DFS.py` is named `BFS` in the source code but implements DFS — it uses `stack.pop()` (LIFO) instead of `queue.pop(0)` (FIFO), which is what distinguishes the two algorithms.

### UCS — Uniform Cost Search (`UCS.py`)
Expands nodes in order of cumulative path cost, using a **priority queue** sorted by total cost at each step.

- Guaranteed to find the **lowest-cost path**
- Generalises BFS to weighted graphs

---

## Graph

All three algorithms run on the same directed graph (unweighted for BFS/DFS, weighted for UCS):

```
        S
      / | \
    A   B   D
    |   |   |
    C   D   G ← goal
   / \  |
  G   D G
```

| Algorithm | Edge weights |
|-----------|-------------|
| BFS / DFS | Unweighted — `{'S': ['A','B','D'], 'A': ['C'], ...}` |
| UCS | Weighted — `{'S': [('A',2),('D',5),('B',3)], ...}` |

**Expected output (BFS/DFS):** A path from `S` to `G`  
**Expected output (UCS):** The lowest-cost path from `S` to `G` with its total cost

---

## Comparison

| Property | BFS | DFS | UCS |
|----------|-----|-----|-----|
| Data structure | Queue (FIFO) | Stack (LIFO) | Priority queue (sorted by cost) |
| Finds shortest path? | Yes (by edges) | No | Yes (by cost) |
| Handles weights? | No | No | Yes |
| Complete? | Yes | Yes (finite graphs) | Yes |
| Time complexity | O(b^d) | O(b^m) | O(b^(C*/ε)) |

*b = branching factor, d = solution depth, m = max depth, C* = optimal cost, ε = min edge cost*

---

## Project Structure

```
graph-search-algorithms/
│
├── BFS.py   # Breadth-First Search
├── DFS.py   # Depth-First Search (note: function misnamed BFS in source)
├── UCS.py   # Uniform Cost Search
└── README.md
```

---

## Requirements

- Python 3.x
- No external libraries — pure Python only

---

## Usage

Run each algorithm independently:

```bash
python BFS.py
python DFS.py
python UCS.py
```

To test on a different graph, modify the `graph` dictionary at the bottom of each file and update the `start` and `goal` arguments in the function call.

---

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Uninformed search** | Searches without domain-specific heuristics — explores purely based on structure or cost |
| **Visited list** | Prevents revisiting nodes to avoid infinite loops in cyclic graphs |
| **Path tracking** | Each queue/stack entry stores the full path, not just the current node, making solution reconstruction immediate |
| **Priority queue (UCS)** | Implemented by sorting the queue by `path_cost` before each pop — ensures the cheapest path is always expanded first |
| **Completeness** | A search algorithm is complete if it always finds a solution when one exists |
| **Optimality** | A search algorithm is optimal if it always finds the lowest-cost solution |
