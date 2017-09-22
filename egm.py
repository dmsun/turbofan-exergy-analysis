import math
import itertools as it

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

from stage_analysis import stage_analysis
from reg_coeff import exergy_regression
from reg_exergy import reg_exergy
from reg_thrust import reg_thrust
from scipy.optimize import minimize
from scipy.stats import norm

np.set_printoptions(suppress=True)
def egm():
    x0 = [1, 1, 1, 1, 1]
    cons = ({'type': 'ineq', 'fun': reg_exergy}),
    bnds = ((-1, 1), (-1, 1), (-1, 1), (-1, 1), (-1, 1))

    max_thrust_input = minimize(reg_thrust, x0, args=(-1.0), bounds = bnds)
    print(max_thrust_input)
    print("\nMax thrust is - ", reg_thrust([1,-1,-1,-1,1]))
    print("Corresponding exergy is - ", reg_exergy([1,-1,-1,-1,1]), "kJ/kg \n \n")

    constrained_max_thrust_input = minimize(reg_thrust, x0, args=(-1.0), bounds = bnds, constraints = cons)
    print(constrained_max_thrust_input)
    print("\nMax thrust for the constrained problem is - ", reg_thrust([1,-1,-1,-1,1]), "m/s")
    print("Corresponding exergy is - ", reg_exergy([1,-1,-1,-1,1]), "kJ/kg \n \n")

    constrained_min_exergy_input = minimize(reg_exergy, x0, args=(1.0), bounds = bnds, constraints = cons)
    print(constrained_min_exergy_input)
    print("\nMin exergy is - ", reg_exergy([1,1,1,1,-1]), "kJ/kg")
    print("Corresponding thrust is - ", reg_thrust([1,1,1,1,-1]), "m/s \n \n")


    #################################################################################
    #################################################################################
    #   how well do the thrust and exergy_destroyed formulas predict the first principle thrust and exergy destroyed?
    print("Computing the test arrays")
    #   number of points want to find - note the time taken to execute is exponential N ^ 5
    N = 10
    #bpr = [5, 6, 7],
    #HPCR = [14, 16, 18],
    #LPCR = [1.5, 2.5, 3.5],
    #M = [0.75, 0.85, 0.95],
    #T_04 = [1400, 1450, 1500]
    bpr = np.linspace(5.1, 6.9, num = N)
    HPCR = np.linspace(13.9, 17.9, num = N)
    LPCR = np.linspace(1.51, 3.49, num = N)
    M = np.linspace(0.76, 0.94, num = N)
    T_04 = np.linspace(1401, 1499, num = N)
    array = list(it.product(bpr, HPCR, LPCR, M, T_04))

    thrust, exergy, __1, __2, __3, __4, __5  = stage_analysis(bpr, HPCR, LPCR, M, T_04)
    bpr_plot = []
    HPCR_plot = []
    LPCR_plot = []
    M_plot = []
    T_04_plot = []
    thrust_regression = []
    thrust_diff = []

    print("Finished running the analysis for the test points, \nnow will create the tranformed variables, and evaluate the regression model")
    for i in range(len(array)):
        test_case = array[i]
        bpr_transform = round((test_case[0] - 6) / (2 / 2), 2)
        HPCR_transform = round((test_case[1] - 16) / (4 / 2), 2)
        LPCR_transform = round((test_case[2] - 2.5) / (2 / 2), 2)
        M_transform = round((test_case[3] - 0.85) / (0.2 / 2), 2)
        T_04_transform = round((test_case[4] - 1450) / (100 / 2), 2)
        bpr_plot.append(bpr_transform)
        HPCR_plot.append(HPCR_transform)
        LPCR_plot.append(LPCR_transform)
        M_plot.append(M_transform)
        T_04_plot.append(T_04_transform)
        thrust_regression.append(reg_thrust([bpr_transform, HPCR_transform, LPCR_transform, M_transform, T_04_transform]))
        thrust_diff.append(thrust[i] - thrust_regression[i])

    # fit the residuals to the gauusian distribution to check for normality.
    mu, sigma = norm.fit(thrust_diff)

    plt.figure(3)
    plt.subplot(331)
    plt.scatter(bpr_plot, thrust)
    m, b = np.polyfit(bpr_plot, thrust, 1)
    y = np.array(bpr_plot) * m + b
    plt.plot(bpr_plot, y, 'r-' )
    plt.xlabel("BPR")
    plt.ylabel("Thrust Observed")

    plt.subplot(332)
    plt.scatter(HPCR_plot, thrust)
    m, b = np.polyfit(HPCR_plot, thrust, 1)
    y = np.array(HPCR_plot) * m + b
    plt.plot(HPCR_plot, y, 'r-' )
    plt.xlabel("HPCR")
    plt.ylabel("Thrust Observed")


    plt.subplot(333)
    plt.scatter(LPCR_plot, thrust)
    m, b = np.polyfit(LPCR_plot, thrust, 1)
    y = np.array(LPCR_plot) * m + b
    plt.plot(LPCR_plot, y, 'r-' )
    plt.xlabel("LPCR")
    plt.ylabel("Thrust Observed")


    plt.subplot(334)
    plt.scatter(M_plot, thrust)
    m, b = np.polyfit(M_plot, thrust, 1)
    y = np.array(M_plot) * m + b
    plt.plot(M_plot, y, 'r-' )
    plt.xlabel("M")
    plt.ylabel("Thrust Observed")

    plt.subplot(335)
    plt.scatter(T_04_plot, thrust)
    m, b = np.polyfit(T_04_plot, thrust, 1)
    y = np.array(T_04_plot) * m + b
    plt.plot(T_04_plot, y, 'r-' )
    plt.xlabel("T_04")
    plt.ylabel("Thrust Observed")

    plt.subplot(336)
    plt.scatter(thrust_regression, thrust)
    m, b = np.polyfit(thrust_regression, thrust, 1)
    y = np.array(thrust_regression) * m + b
    plt.plot(thrust_regression, y, 'r-' )
    plt.xlabel("Predicted Value - Thrust Regression")
    plt.ylabel("Thrust Observed")

    plt.subplot(337)
    plt.scatter(thrust_regression, thrust_diff)
    plt.plot(thrust_regression, [0]*len(thrust_regression), 'r-')
    plt.xlabel("Predicted Value - Thrust Regression")
    plt.ylabel("Thrust (Residual)")

    ax = plt.subplot(338)
    n, bins, patches = plt.hist(thrust_diff, bins = 50, normed = True)
    y = mlab.normpdf(bins, mu, sigma)
    l = plt.plot(bins, y, 'r--', linewidth = 2)
    ax.set_title("Residual plot - $\mu$ = {0} and $\sigma$ = {1}".format(round(mu,2), round(sigma,2)))
    plt.xlabel("Thrust Residual")
    plt.ylabel("Percent")
    plt.show()
egm()
