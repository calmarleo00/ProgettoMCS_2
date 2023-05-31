import numpy as np
import scipy as sp
import math
from scipy.fftpack import dct, idct

from numpy import double


def dct2(a):
    return dct(dct(a.T, norm='ortho').T, norm='ortho')


def cos_series(N, frequence):
    w = np.zeros((N, 1), dtype=double)
    for i in range(0, N):
        w[i] = math.cos((frequence * math.pi) * ((2 * i + 1) / (2 * N)))

    return w


def summatory_b(matrixA, dim, s, r):
    sum = 0
    for i in range(0, dim):
        sum_j = 0
        for j in range(0, dim):
            sum_j = sum_j + (matrixA[i, j] *
                             math.cos(r * math.pi * (((2 * j) + 1) /
                                                     (2 * dim))))
        sum = sum + (math.sqrt(1 / (np.transpose(cos_series(dim, r)).dot(cos_series(dim, r)))) * sum_j * (
            math.cos(s * math.pi * ((2 * i + 1) / (2 * dim)))))
    return sum


if __name__ == "__main__":
    dimension = 8
    # matrixA = np.mat('[1 2; 3 4]')
    matrixA = np.mat('[231 32 233 161 24 71 140 245;'
                     '247 40 248 245 124 204 36 107;'
                     '234 202 245 167 9 217 239 173;'
                     '193 190 100 167 43 180 8 70;'
                     '11 24 210 177 81 243 8 112;'
                     '97 195 203 47 125 114 165 181;'
                     '193 70 174 167 41 30 127 245;'
                     '87 149 57 192 65 129 178 228]')
    array_W = []
    matrixRes = np.ndarray(shape=(dimension, dimension))
    vectorRes = np.ndarray(shape=(1, dimension))

    iteration = 0
    row = 0
    col = 0
    matrixW = np.ndarray(shape=(dimension, dimension))
    while row < dimension:
        while col < dimension:
            matrixRes[row, col] = math.sqrt(
                1 / (np.transpose(cos_series(dimension, row)).dot(cos_series(dimension, row)))) * \
                                  (summatory_b(matrixA, dimension, row, col))

            iteration = iteration + 1
            col = col + 1
        row = row + 1
        col = 0

    print("DCT2:\n")
    print(str(matrixRes))

    print("Library's DCT2:\n")
    imF = dct2(matrixA)
    print(imF)



