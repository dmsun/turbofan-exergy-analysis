from reg_coeff import exergy_regression
def reg_exergy(y, sign = 1.0):
    thrust, exergy = exergy_regression()
    return 1  * (   exergy[0] +
                    exergy[1] * y[0] +
                    exergy[2] * y[1] +
                    exergy[3] * y[2] +
                    exergy[4] * y[3] +
                    exergy[5] * y[4] +
                    exergy[6] * y[0] * y[1] +
                    exergy[7] * y[0] * y[2] +
                    exergy[8] * y[0] * y[3] +
                    exergy[9] * y[0] * y[4] +
                    exergy[10] * y[1] * y[2] +
                    exergy[11] * y[1] * y[3] +
                    exergy[12] * y[1] * y[4] +
                    exergy[13] * y[2] * y[3] +
                    exergy[14] * y[2] * y[4] +
                    exergy[15] * y[3] * y[4] +
                    exergy[16] * y[0] * y[0] +
                    exergy[17] * y[1] * y[1] +
                    exergy[18] * y[2] * y[2] +
                    exergy[19] * y[3] * y[3] +
                    exergy[20] * y[4] * y[4]
                    )
