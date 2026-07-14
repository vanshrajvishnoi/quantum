from dataclasses import dataclass
from typing import List

@dataclass
class BenchmarkResult:
    problem_size: int         
    classical_ops: int     
    quantum_ops: int         
    quantum_qubits: int      

class MetricTracker:
    def __init__(self):
        self.results: List[BenchmarkResult] = []

    def log(self, problem_size: int, classical_ops: int, quantum_ops: int, quantum_qubits: int):
        self.results.append(BenchmarkResult(
            problem_size=problem_size,
            classical_ops=classical_ops,
            quantum_ops=quantum_ops,
            quantum_qubits=quantum_qubits
        ))