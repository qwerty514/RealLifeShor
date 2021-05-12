from credi import GetCredi
from Shor import ShorCircuit
from qiskit import IBMQ, QuantumCircuit, assemble, transpile

provider = IBMQ.enable_account(GetCredi())  #API Token in file ignored by git
backend = provider.get_backend("ibmq_16_melbourne") #only melbourne fits the circuit

testcircuit = ShorCircuit()
testcircuit = transpile(testcircuit, backend)

job = backend.run(testcircuit)
print(job.job_id)

print(job.result())
