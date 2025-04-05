import os
import matplotlib.pyplot as plt
from datetime import datetime
import seater
import file_handler

def run_benchmark(guests, params, n_runs=10):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    benchmark_folder = os.path.join("benchmarks", f"benchmark_{timestamp}")
    os.makedirs(benchmark_folder, exist_ok=True)

    best_costs = []
    scores = []
    folders = []

    for i in range(n_runs):
        print(f"Benchmark Run {i+1}/{n_runs}")
        
        if params["algorithm"] == "Simulated Annealing":
            tables = seater.simulated_annealing(
                guests=guests,
                initial_temperature=params["initial_temperature"],
                cooling_rate=params["cooling_rate"],
                iterations=params["iterations"],
                cooling_type=params["cooling_type"],
                min_per_table=params["min_per_table"],
                max_per_table=params["max_per_table"]
            )
        elif params["algorithm"] == "Genetic Algorithm":
            tables = seater.genetic_algorithm(
                guests=guests,
                min_per_table=params["min_per_table"],
                max_per_table=params["max_per_table"],
                generations=params["iterations"],
                mutation_rate=params["mutation_rate"],
                population_size=params["population_size"]
            )
        # ... outros algoritmos se quiseres

        cost = seater.calculate_cost(tables, guests)
        score = -cost
        perfect_score = seater.calculate_theoretical_perfect_score(guests)
        optimality = (score / perfect_score) * 100 if perfect_score else 0

        # Guardar resultados individuais
        run_folder = os.path.join(benchmark_folder, f"run_{i+1}")
        os.makedirs(run_folder, exist_ok=True)
        file_handler.write_seating_arrangement(
            tables,
            filename=os.path.join(run_folder, "seating.txt"),
            current_score=score,
            perfect_score=perfect_score,
            optimality=optimality,
            algorithm=params["algorithm"]
        )

        best_costs.append(cost)
        scores.append(score)
        folders.append(run_folder)

    # Criar ficheiro resumo
    summary_path = os.path.join(benchmark_folder, "results.txt")
    with open(summary_path, "w") as f:
        f.write("Benchmark Summary\n")
        f.write("=================\n")
        f.write(f"Algorithm: {params['algorithm']}\n")
        f.write(f"Runs: {n_runs}\n\n")
        for i in range(n_runs):
            f.write(f"Run {i+1}:\n")
            f.write(f"  Cost: {best_costs[i]}\n")
            f.write(f"  Score: {scores[i]}\n")
            f.write(f"  Optimality: {scores[i] / perfect_score * 100:.2f}%\n")
            f.write(f"  Folder: {folders[i]}\n\n")
        f.write(f"Average Score: {sum(scores)/n_runs:.2f}\n")
        f.write(f"Best Score: {max(scores)}\n")
        f.write(f"Best Cost: {min(best_costs)}\n")

    # Criar boxplot
    plt.figure(figsize=(6, 6))
    plt.boxplot(best_costs, vert=True, patch_artist=True)
    plt.title(f"{params['algorithm']} - Cost Distribution over {n_runs} Runs")
    plt.ylabel("Final Cost")
    plt.grid(True)
    plt.savefig(os.path.join(benchmark_folder, "boxplot.png"))
    plt.close()

    print(f"Benchmark concluído em {benchmark_folder}")
