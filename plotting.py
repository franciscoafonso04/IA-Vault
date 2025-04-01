import matplotlib.pyplot as plt
import os

def plot_performance_metrics(metrics, save_dir="results"):
    """Plot performance metrics from simulated annealing."""
    os.makedirs(save_dir, exist_ok=True)
    timestamp = metrics['timestamp']
    
    # Create figure with multiple subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
    
    # Plot 1: Cost over iterations
    ax1.plot(metrics['iterations'], metrics['costs'], 'b-', label='Cost')
    ax1.plot(metrics['iterations'], metrics['best_costs'], 'r--', label='Best Cost')
    ax1.set_xlabel('Iteration')
    ax1.set_ylabel('Cost')
    ax1.set_title('Cost Evolution')
    ax1.legend()
    ax1.grid(True)
    
    # Plot 2: Temperature over iterations
    ax2.plot(metrics['iterations'], metrics['temperatures'], 'g-')
    ax2.set_xlabel('Iteration')
    ax2.set_ylabel('Temperature')
    ax2.set_title('Temperature Decay')
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, f'performance_{timestamp}.png'))
    plt.close()
