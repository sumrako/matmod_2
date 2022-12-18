import numpy as np


def dF(N, M, a, b, d, c):
    return N * (a + c * M), M * (b + d * N)
    # return a + c * M + d * M, b + c * N + d * N


def generate_default_popul_data(count: int):
    count_of_popul = [i * 100 for i in range(1, count + 1)]

    growth = [0.01]
    growth[1:] = [-0.01 for _ in range(1, count)]

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
    def __init__(self, a: np.ndarray, B: np.ndarray, N: np.ndarray):
        self.a = a
        self.B = B
        # self.curN = np.copy(N)
        # self.curN = np.float_(self.curN)
        self.beginN = N
        self.N_matrix = None

    def get_N_matrix(self, time: int = 1000, ht: int = 1) -> np.ndarray:
        self.reset_count(time, ht)
        for k in range(1, int(time / ht) + 1):
            for i in range(len(self.beginN)):
                beta_array = np.array([self.B[i, j] * self.N_matrix[j, k-1] * self.N_matrix[i, k-1]
                                       for j in range(len(self.beginN))])
                sum_ = np.sum(beta_array)
                self.N_matrix[i, k] = self.N_matrix[i, k-1] + ht * (self.a[i] * self.N_matrix[i, k-1] + sum_)
        return self.N_matrix

    def set_a(self, a: np.ndarray):
        self.a = a

    def set_B(self, B: np.ndarray):
        self.B = B

    def set_N(self, N: np.ndarray):
        self.beginN = N

    def reset_count(self, time: int, step: int):
        self.N_matrix = np.zeros((len(self.beginN), int(time / step) + 1), dtype=float)
        self.N_matrix[:, 0] = self.beginN

