from credi import GetCredi
from Shor import ShorCircuit, PostProcess
from qiskit import IBMQ, QuantumCircuit, assemble, transpile, Aer
from qiskit.visualization import plot_histogram

def Simulate:
    qasm_sim = Aer.get_backend('qasm_simulator')
    t_qc = transpile(ShorCircuit(), qasm_sim)
    qobj = assemble(t_qc)
    results = qasm_sim.run(qobj).result()
    PostProcess(results.get_counts())

def Excecute:
    provider = IBMQ.enable_account(GetCredi())  #API Token in file ignored by git
    backend = provider.get_backend("ibmq_16_melbourne") #only melbourne fits the circuit

    testcircuit = ShorCircuit()
    testcircuit = transpile(testcircuit, backend)

    job = backend.run(testcircuit)
    print(job.job_id)

    print(job.result())
    PostProcess(job.result.get_counts())
