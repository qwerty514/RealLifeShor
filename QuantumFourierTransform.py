#file: QuantumFourierTransform.py
#authors: Kamiel Fokkink, Bram Mak

#This code implements the quantum fourier transform on a given list of qubits

import cirq

def QFT(qubits):
    circuit = cirq.Circuit()

    n = len(qubits)
    for i, q in enumerate(qubits):
        circuit.append(cirq.H(q))
        for i2 in range(1,n-i):
            circuit.append((cirq.S(q)**(2**-(i2-1))).controlled_by(qubits[i2+i]))
    if (len(qubits)%2==0):
        for i in range(int(len(qubits)/2)):
            circuit.append(cirq.SWAP(qubits[i],qubits[-i-1]))
    else:
        for i in range(int(float(len(qubits)/2) - 0.5)):
            circuit.append(cirq.SWAP(qubits[i],qubits[-i-1]))

    return circuit