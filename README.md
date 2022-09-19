# Quantum-Computing
Toy models in Qiskit: Grover's algorithm with unknown number of solutions and arbitrary number of qubits

## Grover's algorithm for $n$ qubits with unknown number of solutions

This python program finds one solution (among an unknown number of solutions $a$).
Suppose there are $N=2^n$ possible states. Theoretical works[^1] show that the number of loops (oracle + diffuser) to find the solutions is $O(\sqrt{N/a})$.
Here, as a ``toy model implementation", the program stops when 1 solution is found.

It's a toy model, so the oracle is simple and marks only the state $|00...0\rangle$ as a solution. We suppose also that there's a way to check if the state with max probability is a solution.

e.g. if n = 10 (i.e. $N=2^{10}$), then the optimal number of loop is approx. 25 (when there is only 1 known solution).
If the number of solutions is unknown (also suppose that $a\leq N/2$, c.f. the proof in the original paper), this program outputs (for example):

```
found some solution: 0000000000
in 52 loops
on average, should be O(32.0)
```

In the program, each measure is done 1 time (i.e. shots=1)

[^1]: https://arxiv.org/pdf/quant-ph/9605034.pdf
