from qiskit import QuantumCircuit, Aer
import numpy as np

def general_diffuser(nqubits):
    '''
    input: number N of qubits
    output: Grover's diffuser (as a quantum circuit)
    '''
    qc = QuantumCircuit(nqubits)

    # rotate s to state 000...0
    qc.h(list(range(nqubits)))

    # instead of marking all states (except 000...0) with factor -1
    # we'll mark only 111...1 with factor -1
    qc.x(list(range(nqubits)))

    # multi-channel Z gate
    qc.h(nqubits-1)
    qc.mct(list(range(nqubits-1)),nqubits-1)
    qc.h(nqubits-1)

    # revert back to initial orientation
    qc.x(list(range(nqubits)))
    qc.h(list(range(nqubits)))

    return qc

# number of qubits
n = 10

# oracle, say 000...0 is the solution
oracle = QuantumCircuit(n)
# mark 000, by doing X first, then mark 111, and revert back to 000
oracle.x(range(n))
oracle.h(n-1)
oracle.mct(list(range(n-1)),n-1)
oracle.h(n-1)
oracle.x(range(n))

# diffuser
diffuser = general_diffuser(n)

# unknown number of solution
m = 1
lmbd = 6/5 # 1 < lambda < 4/3
solution = '0'*n # suppose there's an easy way to check solutions

# on average the algorithm needs O(sqrt(n/a)) number of "oracle+diffuser" loop
# where a is the (unknown) number of solutions
count = 0 # it'll count the number of loops

while True:

    k = np.random.randint(1,int(m)+1)

    # compose Grover's circuit
    grover = QuantumCircuit(n)
    grover.h(list(range(n))) # create s
    for _ in range(k): # optimal is (0.5*pi/arcsin(1/sqrt(2^n))-1)/2 for 1 known solution
        grover = grover.compose(oracle)
        grover = grover.compose(diffuser)
        count += 1
    grover.measure_all()

    # run simulations
    sim = Aer.get_backend('aer_simulator')
    result = sim.run(grover, shots=1).result().get_counts() # only 1 shot

    potential_solution = list(result.items())[0][0]

    if potential_solution == solution:
        print(f'found some solution: {potential_solution}')
        print(f'in {count} loops')
        print(f'on average, should be O({np.sqrt(2**n)})')
        break

    m = np.min([lmbd*m, np.sqrt(2**n)])
    print(count)
