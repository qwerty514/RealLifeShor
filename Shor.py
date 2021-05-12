#file: main.py
#authors: Kamiel Fokkink, Bram Mak

#This code implements Shors algorithm

from QuantumFourierTransform import QFT
from ControlledMultiplication import c_amod15
from qiskit import QuantumCircuit, Aer, transpile, assemble
from qiskit.visualization import plot_histogram
from fractions import Fraction
import pandas as pd

def ShorCircuit():
    n_count = 8  # number of counting qubits
    a = 7

    qc = QuantumCircuit(n_count + 4, n_count)

    # Initialise counting qubits
    # in state |+>
    for q in range(n_count):
        qc.h(q)

    # And auxiliary register in state |1>
    qc.x(3+n_count)

    # Do controlled-U operations
    for q in range(n_count):
        qc.append(c_amod15(a, 2**q),
                 [q] + [i+n_count for i in range(4)])

    # Do inverse-QFT
    qc.append(QFT(n_count), range(n_count))

    # Measure circuit
    qc.measure(range(n_count), range(n_count))
    qc.draw(fold=-1)  # -1 means 'do not fold'

    return qc

#plot_histogram(counts) Do this to see a histogram of the counts

def PostProcess(resultCounts):
    n_count = 8  # number of counting qubits
    measured_phases = []
    for output in resultCounts:
        decimal = int(output, 2)  # Convert (base 2) string to decimal
        phase = decimal/(2**n_count)  # Find corresponding eigenvalue
        measured_phases.append(phase)

    rows = []
    for phase in measured_phases:
        frac = Fraction(phase).limit_denominator(15)
        rows.append([phase, f"{frac.numerator}/{frac.denominator}", frac.denominator])
    headers=["Phase", "Fraction", "Guess for r"]
    df = pd.DataFrame(rows, columns=headers)
    #print(df) to see the final results

qasm_sim = Aer.get_backend('qasm_simulator')
t_qc = transpile(ShorCircuit(), qasm_sim)
qobj = assemble(t_qc)
results = qasm_sim.run(qobj).result()
counts = results.get_counts()