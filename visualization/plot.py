import matplotlib.pyplot as plt
from core.metrics import MetricTracker

class BenchmarkPlotter:
    @staticmethod
    def render_dashboard(grover_tracker: MetricTracker, shor_tracker: MetricTracker, output_filename="chart.png"):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle('Quantum vs. Classical Complexity', fontsize=16, fontweight='bold')

        g_sizes = [r.problem_size for r in grover_tracker.results]
        g_class = [r.classical_ops for r in grover_tracker.results]
        g_quant = [r.quantum_ops for r in grover_tracker.results]

        ax1.plot(g_sizes, g_class, 'r--o', linewidth=2, label='Classical Linear Search O(N)')
        ax1.plot(g_sizes, g_quant, 'b-s', linewidth=2, label='Grover Quantum Search O(√N)')
        ax1.set_title('Unstructured Search', fontsize=12, fontweight='bold')
        ax1.set_xlabel('Search Space Size (N)', fontsize=11)
        ax1.set_ylabel('Required Queries ', fontsize=11)
        ax1.set_yscale('linear')
        ax1.grid(True, which="both", ls="--", alpha=0.5)
        ax1.legend(loc='upper left', frameon=True)

        s_bits = [r.problem_size for r in shor_tracker.results]
        s_class = [2**b for b in s_bits]
        s_quant = [r.quantum_ops for r in shor_tracker.results] 

        ax2.plot(s_bits, s_class, 'r--o', linewidth=2, label='Classical Search O(2^b)')
        ax2.plot(s_bits, s_quant, 'g-^', linewidth=2, label='Quantum Phase Estimation O(b³)')
        ax2.set_title('Period Finding ', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Precision Bits (b)', fontsize=11)
        ax2.set_ylabel('Operation Count ', fontsize=11)
        ax2.set_yscale('log')
        ax2.grid(True, which="both", ls="--", alpha=0.5)
        ax2.legend(loc='upper left', frameon=True)

        plt.tight_layout()
        plt.savefig(output_filename, dpi=300)
        print(f"\nVisualization exported to '{output_filename}'")