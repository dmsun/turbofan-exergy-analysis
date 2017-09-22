import math
import numpy as np
from stage_analysis import stage_analysis

def exergy_regression(  bpr = [5, 6, 7],
                        HPCR = [14, 16, 18],
                        LPCR = [1.5, 2.5, 3.5],
                        M = [0.75, 0.85, 0.95],
                        T_04 = [1400, 1450, 1500]):

    F_n, X_des, bpr_r, HPCR_r, LPCR_r, M_r, T_04_r = stage_analysis(bpr, HPCR, LPCR, M, T_04)
    #   Begin the Regression Analysis
    R = []
    for i in range(len(F_n)):
        #   residual or error coeffecient is always 1
        error = 1
        #   input variables - need to parameterise the transformation for Design of Experiments
        bpr = int(round((bpr_r[i] - 6) / (2 / 2)))
        HPCR = int(round((HPCR_r[i] - 16) / (4 / 2)))
        LPCR = int(round((LPCR_r[i] - 2.5) / (2 / 2)))
        M = int(round((M_r[i] - 0.85) / (0.2 / 2)))
        T_04 = int(round((T_04_r[i] - 1450) / (100 / 2)))

        #   interaction terms - only single interaction terms
        bpr1 = bpr * HPCR
        bpr2 = bpr * LPCR
        bpr3 = bpr * M
        bpr4 = bpr * T_04

        HPCR1 = HPCR * LPCR
        HPCR2 = HPCR * M
        HPCR3 = HPCR * T_04

        LPCR1 = LPCR * M
        LPCR2 = LPCR * T_04

        M1 = M * T_04

        #    squared variables
        bpr_sq = bpr ** 2
        HPCR_sq = HPCR ** 2
        LPCR_sq = LPCR ** 2
        M_sq = M ** 2
        T_04_sq = T_04 ** 2

        R.append([error, bpr, HPCR, LPCR, M, T_04,
                bpr1, bpr2, bpr3, bpr4,
                HPCR1, HPCR2, HPCR3,
                LPCR1, LPCR2,
                M1,
                bpr_sq, HPCR_sq, LPCR_sq, M_sq, T_04_sq])
    R_trans = np.transpose(R)
    R_sq = np.dot(R_trans, R)
    #   calculate R'y (y is output vector)
    R_transFn = np.dot(R_trans, F_n)
    R_transXdes = np.dot(R_trans, X_des)

    #   calculate the least squares estimates for the regression coefficients of thrust and exergy destroyed
    beta_Fn, __, ____, ____ = np.linalg.lstsq(R_sq, R_transFn)
    beta_Xdes, __, ___, ____ = np.linalg.lstsq(R_sq, R_transXdes)
    #   round values in array to preserve significant values
    beta_Fn = np.around(beta_Fn, 2)
    beta_Xdes = np.around(beta_Xdes, 2)
    return beta_Fn, beta_Xdes
