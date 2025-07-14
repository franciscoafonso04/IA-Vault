# 💍 Wedding Seater Planner

An interactive optimization tool to generate ideal seating arrangements for wedding guests, based on their preferences and constraints.

📌 **Grade received: 19.0/20**

---

## 📘 Project Overview

This application was developed for the Artificial Intelligence and Reasoning Techniques (IART) course at FEUP (2024/25). It applies metaheuristic algorithms to optimize table assignments for wedding guests, ensuring satisfaction and balance based on their stated preferences.

A graphical interface was built using **Pygame**, enabling users to:
- Load a guest list with preferences.
- Adjust algorithm parameters interactively.
- Generate and retry seating plans.
- Benchmark algorithms and visualize comparative performance.

---

## 🧠 Implemented Algorithms

- **Simulated Annealing** — Main algorithm: explores the solution space using a probabilistic acceptance criterion based on temperature and cooling schedule.
- **Genetic Algorithm** — Evolves a population of seating arrangements using crossover and mutation.
- **Hill Climbing** — Fast and greedy baseline that iteratively improves the seating configuration.

---

## 🎯 Features

- **Seating Arrangement Generation**  
  Optimizes guest distribution across tables while satisfying preference constraints.

- **Interactive Parameter Adjustment**  
  Easily configurable algorithm parameters through a Pygame-based menu.

- **Benchmarking Mode**  
  Executes an algorithm multiple times (default: 10), storing outputs and generating performance plots.

- **Algorithm Comparison**  
  Automatically runs all algorithms and visualizes their results with boxplots and metrics.

- **Graphical Visualization**  
  Real-time seating layouts and performance graphs generated using Matplotlib.

---

## 📁 Files Included

```

📁 results/           # Individual seating outputs
📁 benchmarks/        # Benchmark runs
📁 comparisons/       # Algorithm comparison results
guest\_list.csv        # Input guest list (CSV format)
main.py               # Main Pygame interface
seater.py             # Metaheuristic algorithm implementations
ui.py                 # Drawing and UI logic
file\_handler.py       # File I/O and folder management
plotting.py           # Matplotlib graph generation
benchmark.py          # Benchmark and comparison logic

```

---

## 📥 Input Format

The input file must be a `.csv` with the following structure:

```
Guest,Together1,Together2,Together3,Apart1,Apart2,Apart3
Alice,Bob,Charlie,David,Eve,Frank,Grace
...
````

Each guest may list other guests they want to sit **together** with or **apart** from. These preferences are used to calculate a fitness score for each arrangement.

---

## ▶️ How to Run

1. Ensure Python 3 and the required libraries are installed:

   ```bash
   pip install pygame matplotlib
  
2. Place your guest list in the project root and name it `guest_list.csv`, or use the graphical interface to add/edit guests.

3. Run the program:

   ```bash
   python3 main.py
   ```

---

## 📊 Output Examples

* **Optimized Seating Plan** → `seating.txt`
* **Algorithm Performance Graph** → `performance.png`
* **Benchmark Result (Boxplot)** → `boxplot.png`
* **Comparison Plot Across Algorithms** → `comparison_boxplot.png`

---

## ✍️ Authors

* Francisco Afonso (up202208115)
* Miguel Caseira (up202207678)
* Pedro Santoos (up202205900) 

---
