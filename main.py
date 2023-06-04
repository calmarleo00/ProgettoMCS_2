import csv
import time
from datetime import datetime
import numpy as np
import scipy as sp
import math
from scipy.fftpack import dct, idct

from numpy import double


def lib_dct2(a):
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

def dct2(dimension, matrixA):
    matrixRes = np.ndarray(shape=(dimension, dimension))

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

    return matrixRes
if __name__ == "__main__":
    #dimension = 8
    '''
    matrixA = np.mat('[231 32 233 161 24 71 140 245;'
                     '247 40 248 245 124 204 36 107;'
                     '234 202 245 167 9 217 239 173;'
                     '193 190 100 167 43 180 8 70;'
                     '11 24 210 177 81 243 8 112;'
                     '97 195 203 47 125 114 165 181;'
                     '193 70 174 167 41 30 127 245;'
                     '87 149 57 192 65 129 178 228]')
    '''
    header = ['dimensione', 'dct2', 'lib_dct2']
    with open('DCT2.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        for i in range(2, 50):
            matrixA = np.random.randint(1, 300, (i,i), dtype = int)
            start_dct2 = time.perf_counter()
            matrixRes = dct2(i, matrixA)
            end_dct2 = time.perf_counter()
            dct2_time = end_dct2 - start_dct2
            print(dct2_time)
            start_lib_dct2 = time.perf_counter()
            imF = dct(dct(matrixA.T, norm='ortho').T, norm='ortho')
            end_lib_dct2 = time.perf_counter()
            lib_dct2_time = end_lib_dct2 - start_lib_dct2

            writer.writerow([i, dct2_time, lib_dct2_time])






