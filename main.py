from credi import GetCredi
from Shor import ShorCircuit, PostProcess
from qiskit import IBMQ, QuantumCircuit, assemble, transpile, Aer
from qiskit.visualization import plot_histogram
import pandas as pd
from pathlib import Path


# Simulate a Shor circuit for a given a, return results immediately
def Simulate(a=7):
    qasm_sim = Aer.get_backend('qasm_simulator')
    t_qc = transpile(ShorCircuit(a), qasm_sim)
    qobj = assemble(t_qc)
    return qasm_sim.run(qobj).result()


# Take an a, generate circuit and run this on IBMQ
# Job ID of the job on IBMQ
def Execute(a=7):
    if Execute.backend is None:
        Execute.provider = IBMQ.enable_account(GetCredi())  # API Token in file ignored by git
        Execute.backend = Execute.provider.get_backend("ibmq_16_melbourne")  # only melbourne fits the circuit

    testcircuit = ShorCircuit(a)
    testcircuit = transpile(testcircuit, Execute.backend)

    job = Execute.backend.run(testcircuit)
    print(job.job_id)
    return job.job_id

aArray = [2, 7, 8, 11, 13]

def ExecuteAll(n, a, amount):
    if a not in aArray:
        exit(1)
    path = "JobIDs/record" + str(n) + ".csv"
    if Path(path).is_file():
        df = pd.read_csv(path)
    else:
        df = pd.DataFrame(columns=["a", "jobID"])

    for _ in range(amount):
        jobID = Execute(a)
        df = df.append({"a": a, "jobID": jobID}, ignore_index=True)

    df.to_csv(path)


# Take a job_id, get the results from IBMQ
# Returns results of the job!
def RetrieveResult(jobID):
    if RetrieveResult.backend is None:
        RetrieveResult.provider = IBMQ.enable_account(GetCredi())  # API Token in file ignored by git
        RetrieveResult.backend = RetrieveResult.get_backend("ibmq_16_melbourne")  # only melbourne fits the circuit
    return RetrieveResult.backend.retrieve_job(jobID).result()


def RetrieveAll(n):
    path = "JobIDs/record" + str(n) + ".csv"
    df = pd.read_csv(path)
    for ID in df["jobID"]:
        print(df[ID][1])
        print(df[ID][0])
        print(RetrieveResult(ID))

Execute.provider = None
Execute.backend = None

print(Simulate(7))

#for a in aArray:
    #ExecuteAll(1, a, 1)
