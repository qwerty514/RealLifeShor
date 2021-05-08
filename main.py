from credi import GetCredi
from qiskit import IBMQ, QuantumCircuit, assemble, transpile

provider = IBMQ.enable_account(GetCredi())  #API Token in file ignored by git
backend = provider.get_backend("ibmq_santiago")

testcircuit = QuantumCircuit(4)
testcircuit.h(0)
testcircuit.cx(0, 1)
testcircuit.cx(0, 2)
testcircuit.x(3)
testcircuit = transpile(testcircuit, backend)

job = backend.run(testcircuit)
print(job.result())
