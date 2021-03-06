"""
    . This will generate the SELECT operator generated by using phase-relative Toffoli gates.
    . The phase-relativeness of the Toffoli gates could be arbitrary. Meaning, any row of the Toffoli matrix could have
its phase chagned. We can manipulate which rows to change phase by passing a lambda function f(x) where f(x) is the
non-zero entry of the x^th row in the Toffoli matrix.
    . Note [1]: We start with SELECT = Identity, so the end result would be the effect of the relative SELECT operator
on every possible state. However, note that, in the PREPARE + SELECT framework, we start with the ancilla bit being |0>,
so essentially, we can ignore rows with ancilla bit being |1> (meaning, when we evaluate the effect of the SELECT operator
on any selector state, we can ignore the phase changes in |j>|1> for all selector |j>).
"""

from sage.all import *
from gates import *

def generate_Xn_gate(bits):
    ans = matrix(CDF, 1)
    ans[0,0] = 1
    for bit in bits:
        if bit == 1:
            ans = ans.tensor_product(X)
        else:
            ans = ans.tensor_product(I)
    return ans

# generate a phase relative Toffoli gate of n_qubits where f(x) is the entry on the x^th row
def generate_phase_relative_Toffoli(n_qubits, f=lambda x: 1):
    ans = matrix(CDF, 2**n_qubits)
    for j in range(2**n_qubits-2):
        ans[j,j] = f(j)
    j = 2**n_qubits
    ans[j-2, j-1] = f(j-2)
    ans[j-1, j-2] = f(j-1)
    return ans

if __name__ == "__main__":
    n_qubits = 4 # The first n_qubits-1 qubits are the selector qubits, while the n_qubits^th qubit is
                 # the ancilla qubit.
    Xn = []
    for j in range(2**(n_qubits-1)):
        bits = bin(j)[2:].zfill(n_qubits-1)
        bits = list(map(int, list(bits)))
        Xn.append(generate_Xn_gate(bits))

    #for k in range(2**(2**n_qubits)): # iterate over all possibilities of phase change of a Toffoli matrix
    for k in {0b1}: # k represents which rows of the Toffoli matrix to change the phase
        flip_set = set()
        for i, j in enumerate(list(map(int, list(bin(k)[2:].zfill(2**n_qubits))))):
            if j == 1:
                flip_set.add(i)
        print("***************************", flip_set)
        Toffoli = generate_phase_relative_Toffoli(n_qubits, lambda x: -1 if x in flip_set else 1)
        arr = [0 for i in range(n_qubits)]
        arr[-1] = 1
        SELECT = matrix.identity(CDF, 2**n_qubits) # [1]
        for j in range(2**(n_qubits-1)):
            print(j)
            if j == 2 or j == 5 or j == 8:
                continue
            SELECT *= Xn[j].tensor_product(I)
            SELECT *= Toffoli
            SELECT *= Toffoli
            SELECT *= Xn[j].tensor_product(I)
            print(SELECT)
            print()
