from credi import GetCredi
from Shor import ShorCircuit, PostProcess
from visualize import makeBarPlots, guessFactors
from qiskit import IBMQ, QuantumCircuit, assemble, transpile, Aer, execute
from qiskit.visualization import plot_histogram
from qiskit.providers.aer import AerSimulator
from qiskit.providers.aer.noise import NoiseModel

import pandas as pd
from pathlib import Path

# Simulate a Shor circuit for a given a, return results immediately
def Simulate(a=7, model=None):
    if model is not None:
        if Execute.backend is None:
            Execute.provider = IBMQ.enable_account(GetCredi())  # API Token in file ignored by git
            Execute.backend = Execute.provider.get_backend(model)  # only melbourne fits the circuit
        noiseModel = NoiseModel.from_backend(Execute.backend)
        #simul = AerSimulator(noise_model=noiseModel)
        coupling = Execute.backend.configuration().coupling_map
        basisGates = noiseModel.basis_gates
        return execute(ShorCircuit(a), Aer.get_backend('qasm_simulator'),
                        coupling_map=coupling,
                        basis_gates=basisGates,
                        noise_model=noiseModel).result()
        #return simul.run(ShorCircuit(a)).result()
    else:
        qasm_sim = Aer.get_backend('qasm_simulator')
        t_qc = transpile(ShorCircuit(a), qasm_sim)
        qobj = assemble(t_qc)
        return qasm_sim.run(qobj).result()

# Run Shor circuit for multiple guesses of a, and save the results as bar charts
# and tables
def SimulateAll():
    results1 = dict()
    results2 = dict()
    for a in aArray:
        df1, counts1 = PostProcess(Simulate(a),a)
        results1[a] = counts1
        guessFactors(df1, a, 15, "Simulation")
        """Fix here to include noise model"""
        df2, counts2 = PostProcess(Simulate(a, model="ibmq_16_melbourne"), a)
        results2[a] = counts2
        guessFactors(df2, a, 15, "NoiseModel")
        #PostProcess(Simulate(a, "ibmq_16_melbourne"), a)
        #PostProcess(Simulate(a, "qasm_simulator"), a)
    makeBarPlots(results1, results2)
    #return results1,results2

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

aArray = [2, 7, 8, 11, 13]

SimulateAll()

#Simulate(7,"ibmq_16_melbourne")