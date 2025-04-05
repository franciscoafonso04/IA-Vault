import os
import matplotlib.pyplot as plt
from datetime import datetime
import seater
import file_handler

def run_benchmark(guests, params, algorithm, n_runs=10):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    benchmark_folder = os.path.join("benchmarks", f"benchmark_{timestamp}_{algorithm.replace(' ', '_').lower()}")
    os.makedirs(benchmark_folder, exist_ok=True)

    best_costs = []
    scores = []
    folders = []

    for i in range(n_runs):
        print(f"[{algorithm}] Benchmark Run {i+1}/{n_runs}")
        
        if algorithm == "Simulated Annealing":
            tables = seater.simulated_annealing(
                guests=guests,
                initial_temperature=params["initial_temperature"],
                cooling_rate=params["cooling_rate"],
                iterations=params["iterations"],
                cooling_type=params["cooling_type"],
                min_per_table=params["min_per_table"],
                max_per_table=params["max_per_table"]
            )
        elif algorithm == "Genetic Algorithm":
            tables = seater.genetic_algorithm(
                guests=guests,
                min_per_table=params["min_per_table"],
                max_per_table=params["max_per_table"],
                generations=params["iterations"],
                mutation_rate=params["mutation_rate"],
                population_size=params["population_size"]
            )
        elif algorithm == "Hill Climbing":
            tables = seater.hill_climbing(
                guests=guests,
                min_per_table=params["min_per_table"],
                max_per_table=params["max_per_table"],
                iterations=params["iterations"]
            )
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")

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
            algorithm=algorithm
        )

        best_costs.append(cost)
        scores.append(score)
        folders.append(run_folder)

    # Criar ficheiro resumo
    summary_path = os.path.join(benchmark_folder, "results.txt")
    with open(summary_path, "w") as f:
        f.write("Benchmark Summary\n")
        f.write("=================\n")
        f.write(f"Algorithm: {algorithm}\n")
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

    # Criar boxplot individual
    plt.figure(figsize=(6, 6))
    plt.boxplot(best_costs, vert=True, patch_artist=True)
    plt.title(f"{algorithm} - Cost Distribution over {n_runs} Runs")
    plt.ylabel("Final Cost")
    plt.grid(True)
    plt.savefig(os.path.join(benchmark_folder, "boxplot.png"))
    plt.close()

    print(f"[✓] Benchmark concluído em: {benchmark_folder}")
    
    return benchmark_folder, best_costs, scores


def compare_algorithms(guests, algorithms_to_test, params, n_runs=10):
    
    # Criar pasta base para comparação
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    comparison_folder = os.path.join("benchmarks", f"comparison_{timestamp}")
    os.makedirs(comparison_folder, exist_ok=True)

    all_costs = {}
    all_scores = {}

    for algo in algorithms_to_test:
        print(f"\n🔍 Benchmarking {algo}...")
        benchmark_folder, costs, scores = run_benchmark(
            guests=guests,
            params=params,
            algorithm=algo,
            n_runs=n_runs
        )

        all_costs[algo] = costs
        all_scores[algo] = scores

        # Mover resultados do benchmark individual para a pasta da comparação
        algo_folder = os.path.join(comparison_folder, algo.replace(" ", "_").lower())
        os.rename(benchmark_folder, algo_folder)

    # Criar gráfico comparativo
    plt.figure(figsize=(8, 6))
    plt.boxplot(all_costs.values(), labels=all_costs.keys())
    plt.title(f"Cost Comparison over {n_runs} Runs")
    plt.ylabel("Final Cost")
    plt.grid(True)
    plt.savefig(os.path.join(comparison_folder, "comparison_boxplot.png"))
    plt.close()

    # Criar resumo em txt
    with open(os.path.join(comparison_folder, "comparison_summary.txt"), "w") as f:
        f.write(f"Comparison Summary ({n_runs} runs)\n")
        f.write("=" * 50 + "\n\n")
        for algo in algorithms_to_test:
            scores = all_scores[algo]
            avg = sum(scores) / len(scores)
            best = max(scores)
            worst = min(scores)
            f.write(f"{algo}:\n")
            f.write(f"  Avg Score: {avg:.2f}\n")
            f.write(f"  Best Score: {best}\n")
            f.write(f"  Worst Score: {worst}\n\n")

    print(f"\n✅ Comparação concluída em: {comparison_folder}")


