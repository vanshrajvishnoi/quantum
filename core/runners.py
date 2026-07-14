import math
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

class QuantumRunner:
    def __init__(self):
        self.simulator = AerSimulator()

    def get_circuit_metrics(self, qc: QuantumCircuit):
        pm = generate_preset_pass_manager(backend=self.simulator, optimization_level=1)
        isa_circuit = pm.run(qc)
        return isa_circuit.depth(), isa_circuit.num_qubits

    def execute(self, qc: QuantumCircuit, shots: int = 1024):
        qc_measured = qc.copy()
        if not qc_measured.clbits:
            qc_measured.measure_all()
        result = self.simulator.run(qc_measured, shots=shots).result()
        return result.get_counts()