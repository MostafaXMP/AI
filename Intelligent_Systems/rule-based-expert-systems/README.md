# rule-based-expert-systems

A Python implementation of two classic **rule-based expert systems**, each demonstrating a different inference strategy: **forward chaining** for car fault diagnosis and **backward chaining** for animal identification. Both systems are interactive, querying the user step by step and printing a full reasoning trace of every rule applied.

---

## Systems

### System 1 — Car Troubleshooting (Forward Chaining)

The user answers yes/no questions about their car's symptoms. The engine collects these as facts, then repeatedly scans the rule base and fires any rule whose conditions are fully satisfied — propagating new facts until no more rules can be triggered.

**Rule base (6 rules):**

| Conditions | Conclusion | Diagnosis |
|------------|------------|-----------|
| engine cranks, no start | `battery_dead` | Weak or dead battery |
| engine doesn't crank + dim lights | `battery_dead` | Battery likely dead |
| battery OK + fuel low | `no_fuel` | Fuel level or pump issue |
| battery OK + fuel OK + no spark | `ignition_problem` | Ignition / coil / plug issue |
| starter clicks + engine doesn't crank | `starter_fault` | Starter motor or solenoid |
| cranks + fuel OK + spark OK | `engine_mechanical_issue` | Timing or compression fault |

Multiple conclusions can be reached in a single session if the facts support them.

**Example session:**
```
Does the engine crank when you turn the key? → no
Do the dashboard lights appear dim?          → yes
Do you hear a single click?                  → yes
...
Conclusions:
- Likely battery problem (battery_dead).
- Likely starter motor/solenoid issue (starter_fault).
```

---

### System 2 — Animal Identification (Backward Chaining)

The system works in reverse: it picks a goal (e.g. "is this a bird?") and tries to prove it by recursively checking whether each required condition is already known or can be established by asking the user. If no rule can prove a goal, the system asks the user directly as a fallback.

**Rule base (8 rules):**

| Conditions | Conclusion |
|------------|------------|
| lays eggs + has feathers | bird |
| flies + has feathers | bird |
| gives milk + has fur | mammal |
| is domestic + gives milk | cow |
| has fins + lives in water | fish |
| has scales + lives in water | fish |
| lays eggs + is aquatic + has scales | reptile or fish |
| has shell + lays eggs | reptile |

The engine works through goals depth-first, only asking the user for facts it cannot derive from rules — avoiding redundant questions.

---

## Inference Strategies Compared

| Property | Forward Chaining | Backward Chaining |
|----------|-----------------|-------------------|
| Direction | Facts → Conclusions | Goal → Sub-goals → Facts |
| Driven by | Available evidence | Hypothesis to prove |
| Best for | Diagnosis / monitoring | Classification / identification |
| Questions asked | All upfront | Only what's needed to prove the goal |

---

## Project Structure

```
rule-based-expert-systems/
│
├── 2_Expert_Systems.ipynb   # Full implementation and interactive demo
└── README.md
```

---

## Requirements

- Python 3.7+
- No external libraries — pure Python only

---

## Usage

Open and run the notebook:

```bash
jupyter notebook 2_Expert_Systems.ipynb
```

Run the final cell to launch the main menu:

```
Expert Systems - Task 2
Choose an option:
1. Run Car Troubleshooting (Forward Chaining)
2. Run Animal Identification (Backward Chaining)
3. Exit
```

Answer each yes/no prompt. After all questions are answered, the system prints the collected facts, every reasoning step taken, and the final conclusions or diagnosis.

---

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Expert system** | A program that emulates the decision-making of a domain expert using a rule base and an inference engine |
| **Rule base** | A set of IF-THEN rules encoding domain knowledge |
| **Forward chaining** | Data-driven inference — starts from known facts and fires rules until no new conclusions can be drawn |
| **Backward chaining** | Goal-driven inference — starts from a hypothesis and works backwards to find supporting facts |
| **Reasoning trace** | A log of every rule considered and every fact derived, providing full explainability |
| **Fact set** | The working memory of the system — grows as new facts are confirmed or derived |
