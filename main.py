from credi import GetCredi
from Shor import ShorCircuit, PostProcess
from qiskit import IBMQ, QuantumCircuit, assemble, transpile, Aer
from qiskit.visualization import plot_histogram
import pandas as pd

# Simulate a Shor circuit for a given a, return results immediately
def Simulate(a=7):
    qasm_sim = Aer.get_backend('qasm_simulator')
    t_qc = transpile(ShorCircuit(a=7), qasm_sim)
    qobj = assemble(t_qc)
    return qasm_sim.run(qobj).result()

# Take an a, generate circuit and run this on IBMQ
# Job ID of the job on IBMQ
def Excecute(a=7):
    provider = IBMQ.enable_account(GetCredi())  #API Token in file ignored by git
    backend = provider.get_backend("ibmq_16_melbourne") #only melbourne fits the circuit

    testcircuit = ShorCircuit(a)
    testcircuit = transpile(testcircuit, backend)

    job = backend.run(testcircuit)
    print(job.job_id)
    return job.job_id

def ExecuteAll(n):
    guesses = [2,7,8,11,13]
    records = []
    for a in guesses:
        for _ in range(3):
            jobID = Execute(a)
            records.append([a,jobID])
    
    df = pd.DataFrame(records,columns=["a","jobID"])
    path = "JobIDs/record" + str(n) + ".csv"
    df.to_csv(path,ignore_index=True)

# Take a job_id, get the results from IBMQ
# Returns results of the job!
def PostExcecute(jobID):
    print(job.result())
