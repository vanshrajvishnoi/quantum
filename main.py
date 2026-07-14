from core.runners import QuantumRunner
from core.metrics import MetricTracker
from comparison.grover_vs_linear import GroverBenchmark
from comparison.shor_vs_factoring import ShorBenchmark
from visualization.plot import BenchmarkPlotter

def main():
    runner = QuantumRunner()
    
    print("\nExecuting Grover's Algorithm ...")
    grover_tracker = MetricTracker()
    grover_bench = GroverBenchmark(runner)
    grover_bench.run_suite(qubit_range=range(2, 7), tracker=grover_tracker)
    
    print(f"{'N Size':<10} | {'Classical Ops':<15} | {'Quantum Oracles':<15} | {'Qubits':<8}")
    print("-" * 55)
    for r in grover_tracker.results:
        print(f"{r.problem_size:<10} | {r.classical_ops:<15} | {r.quantum_ops:<15} | {r.quantum_qubits:<8}")

    print("\n Executing Shor's Algorithm ...")
    shor_tracker = MetricTracker()
    shor_bench = ShorBenchmark(runner)
    shor_bench.run_suite(bit_sizes=range(3, 8), tracker=shor_tracker)
    
    print(f"{'Bits (b)':<10} | {'Classical Mod Ops':<18} | {'QPE Circuit Depth':<18} | {'Qubits':<8}")
    print("-" * 60)
    for r in shor_tracker.results:
        print(f"{r.problem_size:<10} | {r.classical_ops:<18} | {r.quantum_ops:<18} | {r.quantum_qubits:<8}")

    BenchmarkPlotter.render_dashboard(grover_tracker, shor_tracker)

if __name__ == "__main__":
    main()