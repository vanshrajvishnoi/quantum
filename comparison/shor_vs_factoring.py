import math
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT
from core.metrics import MetricTracker
from core.runners import QuantumRunner

class ShorBenchmark:
    def __init__(self, runner: QuantumRunner):
        self.runner = runner

    def _classical_period_finding(self, a: int, N: int) -> int:
        r = 1
        ops = 0
        while True:
            ops += 1
            if pow(a, r, N) == 1:
                return ops
            r += 1

    def _build_qpe_circuit(self, num_counting_qubits: int) -> QuantumCircuit:
        total_qubits = num_counting_qubits + 1  # Counting qubits + 1 target qubit
        qc = QuantumCircuit(total_qubits)
        
        qc.h(range(num_counting_qubits))        
        qc.x(num_counting_qubits)
        
        for i in range(num_counting_qubits):
            qc.cp(math.pi / (2**i), i, num_counting_qubits)
            
        inv_qft = QFT(num_qubits=num_counting_qubits, inverse=True, do_swaps=True).to_gate()
        qc.append(inv_qft, range(num_counting_qubits))        
        return qc

    def run_suite(self, bit_sizes: range, tracker: MetricTracker):
        a, N = 7, 15 
        
        for bits in bit_sizes:
            classical_ops = self._classical_period_finding(a, N)
            qc = self._build_qpe_circuit(num_counting_qubits=bits)
            depth, total_qubits = self.runner.get_circuit_metrics(qc)
            
            tracker.log(
                problem_size=bits,
                classical_ops=classical_ops,
                quantum_ops=depth,  
                quantum_qubits=total_qubits
            )