import matplotlib.pyplot as plt
import os

# ============================================================================================================================================================
# Função: plot_performance_metrics
# Descrição: Gera 4 gráficos em subplots para o algoritmo Simulated Annealing.
#            Salva a figura como "performance.png" na pasta indicada.
# ============================================================================================================================================================

def plot_performance_metrics(metrics, save_dir="results"):
    os.makedirs(save_dir, exist_ok=True)

    # Extrair listas de métricas
    iterations = metrics['iterations']
    costs = metrics['costs']
    best_costs = metrics['best_costs']
    temperatures = metrics['temperatures']

    # Calcular variação de custo entre iterações
    delta_costs = [costs[i] - costs[i-1] for i in range(1, len(costs))]
    delta_costs.insert(0, 0)  # A primeira iteração não tem delta

    # Criar figura com 4 subplots
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Simulated Annealing Metrics", fontsize=16)

    # 1. Gráfico: Custo ao longo das iterações
    axs[0, 0].plot(iterations, costs, label='Cost', color='blue')
    axs[0, 0].plot(iterations, best_costs, label='Best Cost', color='red', linestyle='--')
    axs[0, 0].set_title("Cost over Iterations")
    axs[0, 0].set_xlabel("Iteration")
    axs[0, 0].set_ylabel("Cost")
    axs[0, 0].legend()
    axs[0, 0].grid(True)

    # 2. Gráfico: Temperatura ao longo das iterações
    axs[0, 1].plot(iterations, temperatures, color='green')
    axs[0, 1].set_title("Temperature Decay")
    axs[0, 1].set_xlabel("Iteration")
    axs[0, 1].set_ylabel("Temperature")
    axs[0, 1].grid(True)

    # 3. Gráfico: Variação do custo por iteração (Δ)
    axs[1, 0].plot(iterations, delta_costs, color='purple')
    axs[1, 0].set_title("Δ Cost per Iteration")
    axs[1, 0].set_xlabel("Iteration")
    axs[1, 0].set_ylabel("Δ Cost")
    axs[1, 0].axhline(0, color='black', linestyle='dotted') # Linha de referência em 0
    axs[1, 0].grid(True)

    # 4. Gráfico: Custo vs Temperatura (scatter)
    axs[1, 1].scatter(temperatures, costs, alpha=0.5, c='orange')
    axs[1, 1].set_title("Cost vs Temperature")
    axs[1, 1].set_xlabel("Temperature")
    axs[1, 1].set_ylabel("Cost")
    axs[1, 1].grid(True)

    # Ajustar layout e salvar figura
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(os.path.join(save_dir, "performance.png"))
    plt.close()

# ============================================================================================================================================================
# Função: plot_hill_climbing_progress
# Descrição: Mostra a evolução do custo durante o Hill Climbing.
# ============================================================================================================================================================

def plot_hill_climbing_progress(costs, save_dir="results"):
    
    os.makedirs(save_dir, exist_ok=True)
    plt.figure(figsize=(6, 4))
    plt.plot(costs, marker='o', linestyle='-', label='Cost per iteration')
    plt.title("Hill Climbing Progress")
    plt.xlabel("Iteration")
    plt.ylabel("Cost")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, "hill_climbing_progress.png"))
    plt.close()

# ============================================================================================================================================================
# Função: plot_genetic_progress
# Descrição: Mostra a evolução do melhor score por geração no Genetic Algorithm.
# ============================================================================================================================================================

def plot_genetic_progress(best_scores, best_costs=None, save_dir="results"):

    os.makedirs(save_dir, exist_ok=True)
    plt.figure(figsize=(8, 5))

    generations = list(range(len(best_scores)))

    plt.plot(generations, best_scores, marker='o', linestyle='-', label='Best Score per Generation', color='green')

    if best_costs:
        plt.plot(generations, best_costs, marker='x', linestyle='--', label='Best Cost per Generation', color='red')

    plt.title("Genetic Algorithm Progress")
    plt.xlabel("Generation")
    plt.ylabel("Score / Cost")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, "genetic_progress.png"))
    plt.close()


