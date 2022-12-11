import numpy as np


def generate_default_popul_data(count: int):
    count_of_popul = [i * 100 for i in range(1, count + 1)]

    growth = [-0.01]
    growth[1:] = [0.01 for _ in range(1, count)]

    assert len(count_of_popul) == len(growth)

    popul_data = (np.array([count_of_popul, growth])).T
    return popul_data


def generate_default_interactions_data(count: int):
    upper = np.full(count, -0.0001)
    lower = np.full(count, 0.0001)

    upper = np.triu(upper)
    lower = np.tril(lower)

    result = upper + lower
    return result


class PopulationInteractionModel:
    def __init__(self, a: np.ndarray, B: np.ndarray, N: np.ndarray, ht: int = 1):
        self.a = a
        self.B = B
        self.beginN = N
        self.N = N
        self.ht = ht

    def get_N_after_step(self) -> np.ndarray:
        for i in range(len(self.N)):
            beta_array = np.array([self.B[i, j] * self.N[j] for j in range(1, len(self.N))])
            sum_ = np.sum(beta_array)
            self.N[i] = self.N[i] / (1 - self.ht * (self.a[i] + sum_))

        return self.N
