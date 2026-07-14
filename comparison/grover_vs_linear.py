import math
from qiskit import QuantumCircuit
from core.metrics import MetricTracker
from core.runners import QuantumRunner

class GroverBenchmark:
    def __init__(self, runner: QuantumRunner):
        self.runner = runner

    def _run_classical_search(self, dataset: list, target: int) -> int:
        queries = 0
        for item in dataset:
            queries += 1
            if item == target:
                break
        return queries

    def _build_grover_circuit(self, num_qubits: int, target_state: int) -> QuantumCircuit:
        qc = QuantumCircuit(num_qubits)
        
        qc.h(range(num_qubits))        
        num_iterations = max(1, math.floor((math.pi / 4) * math.sqrt(2**num_qubits)))
        
        for _ in range(num_iterations):
            # 2. Oracle (Phase Flip for Target State)
            binary_target = format(target_state, f'0{num_qubits}b')
            for i, bit in enumerate(binary_target):
                if bit == '0':
                    qc.x(i)
            
            if num_qubits > 1:
                qc.mcp(math.pi, list(range(num_qubits - 1)), num_qubits - 1)
            else:
                qc.z(0)
                
            for i, bit in enumerate(binary_target):
                if bit == '0':
                    qc.x(i)
            
            qc.h(range(num_qubits))
            qc.x(range(num_qubits))
            if num_qubits > 1:
                qc.mcp(math.pi, list(range(num_qubits - 1)), num_qubits - 1)
            else:
                qc.z(0)
            qc.x(range(num_qubits))
            qc.h(range(num_qubits))
            
        return qc, num_iterations

    def run_suite(self, qubit_range: range, tracker: MetricTracker):
        for num_qubits in qubit_range:
            N = 2**num_qubits
            dataset = list(range(N))
            target = N - 1              
            classical_queries = self._run_classical_search(dataset, target)
            
            qc, iterations = self._build_grover_circuit(num_qubits, target)
            depth, total_qubits = self.runner.get_circuit_metrics(qc)
            
            tracker.log(
                problem_size=N,
                classical_ops=classical_queries,
                quantum_ops=iterations,  
                quantum_qubits=total_qubits
            )