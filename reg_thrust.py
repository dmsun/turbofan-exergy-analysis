from reg_coeff import exergy_regression
def reg_thrust(x, sign = 1.0):
    thrust, exergy = exergy_regression()
    return sign * ( thrust[0] +
                    thrust[1] * x[0] +
                    thrust[2] * x[1] +
                    thrust[3] * x[2] +
                    thrust[4] * x[3] +
                    thrust[5] * x[4] +
                    thrust[6] * x[0] * x[1] +
                    thrust[7] * x[0] * x[2] +
                    thrust[8] * x[0] * x[3] +
                    thrust[9] * x[0] * x[4] +
                    thrust[10] * x[1] * x[2] +
                    thrust[11] * x[1] * x[3] +
                    thrust[12] * x[1] * x[4] +
                    thrust[13] * x[2] * x[3] +
                    thrust[14] * x[2] * x[4] +
                    thrust[15] * x[3] * x[4] +
                    thrust[16] * x[0] * x[0] +
                    thrust[17] * x[1] * x[1] +
                    thrust[18] * x[2] * x[2] +
                    thrust[19] * x[3] * x[3] +
                    thrust[20] * x[4] * x[4]
                    )
