#file: QuantumFourierTransform.py
#authors: Kamiel Fokkink, Bram Mak

#This code implements the quantum fourier transform on a given on a circuit
#with amount of qubits given by qubits
    
import qiskit as qs
import numpy as np

def QFT(qubits):
    circuit = qs.QuantumCircuit(qubits)
    
    for qubit in range(qubits//2):
        circuit.swap(qubit,qubits-qubit-1)
    for j in range(qubits):
        for m in range(j):
            circuit.cp(-np.pi/float(2**(j-m)), m, j)
        circuit.h(j)
        
    return circuit