from credi import GetCredi
from Shor import ShorCircuit, PostProcess
from qiskit import IBMQ, QuantumCircuit, assemble, transpile, Aer
from qiskit.visualization import plot_histogram

provider = None
backend = None

# Simulate a Shor circuit for a given a, return results immediately
def Simulate(a=7):
    qasm_sim = Aer.get_backend('qasm_simulator')
    t_qc = transpile(ShorCircuit(a=7), qasm_sim)
    qobj = assemble(t_qc)
    return qasm_sim.run(qobj).result()

# Take an a, generate circuit and run this on IBMQ
# Job ID of the job on IBMQ
def Excecute(a=7):
    if Excecute.backend is None:
        Excecute.provider = IBMQ.enable_account(GetCredi())  #API Token in file ignored by git
        Excecute.backend = provider.get_backend("ibmq_16_melbourne") #only melbourne fits the circuit

    testcircuit = ShorCircuit(a)
    testcircuit = transpile(testcircuit, backend)

    job = Excecute.backend.run(testcircuit)
    print(job.job_id)
    return job.job_id


# Take a job_id, get the results from IBMQ
# Returns results of the job!
def PostExcecute(jobID):
    if PostExcecute.backend is None:
        PostExcecute.provider = IBMQ.enable_account(GetCredi())  #API Token in file ignored by git
        PostExcecute.backend = PostExcecute.get_backend("ibmq_16_melbourne") #only melbourne fits the circuit
    return PostExcecute.backend.retrieve_job(jobID).result()
