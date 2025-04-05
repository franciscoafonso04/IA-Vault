import matplotlib.pyplot as plt
import os

def plot_performance_metrics(metrics, save_dir="results"):
    os.makedirs(save_dir, exist_ok=True)

    iterations = metrics['iterations']
    costs = metrics['costs']
    best_costs = metrics['best_costs']
    temperatures = metrics['temperatures']

    # Calcular as melhorias (delta cost)
    delta_costs = [costs[i] - costs[i-1] for i in range(1, len(costs))]
    delta_costs.insert(0, 0)  # Primeira iteração não tem delta

    # Início do gráfico
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Simulated Annealing Metrics", fontsize=16)

    # 1. Cost vs Iteration
    axs[0, 0].plot(iterations, costs, label='Cost', color='blue')
    axs[0, 0].plot(iterations, best_costs, label='Best Cost', color='red', linestyle='--')
    axs[0, 0].set_title("Cost over Iterations")
    axs[0, 0].set_xlabel("Iteration")
    axs[0, 0].set_ylabel("Cost")
    axs[0, 0].legend()
    axs[0, 0].grid(True)

    # 2. Temperature vs Iteration
    axs[0, 1].plot(iterations, temperatures, color='green')
    axs[0, 1].set_title("Temperature Decay")
    axs[0, 1].set_xlabel("Iteration")
    axs[0, 1].set_ylabel("Temperature")
    axs[0, 1].grid(True)

    # 3. Delta Cost (mudança em relação à iteração anterior)
    axs[1, 0].plot(iterations, delta_costs, color='purple')
    axs[1, 0].set_title("Δ Cost per Iteration")
    axs[1, 0].set_xlabel("Iteration")
    axs[1, 0].set_ylabel("Δ Cost")
    axs[1, 0].axhline(0, color='black', linestyle='dotted')
    axs[1, 0].grid(True)

    # 4. Cost vs Temperature (scatter)
    axs[1, 1].scatter(temperatures, costs, alpha=0.5, c='orange')
    axs[1, 1].set_title("Cost vs Temperature")
    axs[1, 1].set_xlabel("Temperature")
    axs[1, 1].set_ylabel("Cost")
    axs[1, 1].grid(True)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(os.path.join(save_dir, "performance.png"))
    plt.close()
