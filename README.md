# 💍 Wedding Seater Planner - Group_A1_78

An interactive optimization tool to generate ideal seating arrangements for wedding guests, based on their preferences and constraints.

## 📌 Project Overview

This application uses metaheuristic algorithms to maximize guest satisfaction and ensure balanced tables. It includes a graphical interface built with Pygame, allowing users to:
- Load a guest list with preferences.
- Adjust algorithm parameters.
- Visualize and retry seating arrangements.
- Run benchmarks and compare algorithms.

## 🧠 Implemented Algorithms

- **Simulated Annealing** (main algorithm): explores the solution space using a probabilistic acceptance criterion.
- **Genetic Algorithm**: evolves a population of seating plans through crossover and mutation.
- **Hill Climbing**: a fast, greedy baseline that iteratively improves the solution.

## 📈 Features

- **Seating Arrangement Generation**  
  Generates optimized table assignments respecting guest preferences and balance constraints.

- **Parameter Adjustment**  
  User-friendly menu to configure algorithm-specific parameters.

- **Benchmarking Mode**  
  Runs the selected algorithm multiple times (default: 10), saving all outputs and generating performance plots.

- **Algorithm Comparison**  
  Executes and compares different algorithms via boxplots and summary metrics.

- **Visual Output**  
  Each result includes `.txt` seating files and performance graphs (PNG).

## 🗂 File Structure

```
📁 results/
📁 benchmarks/
📁 comparisons/
guest_list.csv         # Input guest list
main.py                # Main Pygame interface
seater.py              # All algorithms and utilities
ui.py                  # Drawing functions for interface
file_handler.py        # File I/O and folder management
plotting.py            # Plot generation (matplotlib)
benchmark.py           # Benchmark and Comparison Functions
```

## 📥 Input Format

The guest list must be in `.csv` format with the following structure:

```
Guest,Together1,Together2,Together3,Apart1,Apart2,Apart3
Alice,Bob,Charlie,David,Eve,Frank,Grace
...
```

Each guest may specify people they would like to sit with (`Together`) or avoid (`Apart`).

## 🧪 Running the Program

1. Make sure you have Python 3 and the required libraries:
   ```
   pip install pygame matplotlib
   ```

2. Place your guest list CSV in the root folder and name it `guest_list.csv`, or edit the current one. Note: You can also add guests through the program interface by going to "View Preferences Table" and then clicking the button "Add Guest".

3. Run the program:
   ```
   python3 main.py
   ```

## 📊 Example Outputs

- **Seating Plan:** `seating.txt`
- **Simulated Annealing Performance:** `performance.png`
- **Benchmark Boxplot:** `boxplot.png`
- **Comparison Plot:** `comparison_boxplot.png`


