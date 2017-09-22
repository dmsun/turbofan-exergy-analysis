#! usr/bin/env python3#! usr/bin/env python3
import math
import numpy as np
import itertools as it
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

def stage_analysis(  bpr = [5, 6, 7],
                        HPCR = [14, 16, 18],
                        LPCR = [1.5, 2.5, 3.5],
                        M = [0.75, 0.85, 0.95],
                        T_04 = [1400, 1450, 1500]):
    #   initilise the regression arrays for each input and output variable
    #   Thrust, Exergy Destroyed, Bypass Ratio, High Pressure Compressor Ratio,
    #   Low Pressure Compression Ratio, Mach Number, and Turbine Inlet Temperature
    F_n = []
    X_des = []
    bpr_r = []
    HPCR_r = []
    LPCR_r = []
    M_r = []
    T_04_r = []
    #   will need to put in some exception raising to determine the validity of input parameters
    #   design FPR = Fan Pressure Ratio
    FPR = 1.8
    K_T = 1.0
    #   Celsius to Kelvin conversion constant
    C_K = 273.15
    #   data gathered using US Atmospheric Tables
    #   Universal Gas Constant
    R_air = 0.287
    #   Polytropic Efficiencies
    #   High Pressure Spool Turbine
    eta_pT_HPS = 0.875
    #   Low Pressure Spool Turbine
    eta_pT_LPS = 0.875
    #   High Pressure Spool Compressor
    eta_pC_HPS = 0.9
    #   Low Pressure Spool Compressor
    eta_pC_LPS = 0.85
    #   Fan
    eta_pF = 0.85
    #   Pressure drop over combustion chamber is assumed to be 5% - maximum value is 1.
    core_pressure_ratio = 0.95
    #   Ideal Gas Assumption
    k_air = 1.4
    cpa = 1.005  #kJ/kgK
    #   Exhaust assumed to be an ideal gas.
    k_exhaust = 1.3
    cpe = 1.244   #kJ/kgK
    c_ve = cpe / k_exhaust #kJ/kgK
    R_e = cpe - c_ve #kJ/kgK
    #   Local Ambient Temperature [K]
    T_2 = 226.73
    #   Reference Temp for enthalpy calculations [K]
    T_ref = 226.73
    #   Design Point Variables
    #   Speed of sound
    a = np.sqrt(k_air * R_air * 1000 * T_2)
    #   Operating altitude
    alt = 31000 #ft
    z = 9448.8 #m
    g = 9.81 #m/s ** 2
    #   free stream conditions. Pressure [kPa], Density [kg/m ** 3], Temperature [K]
    P_air = 0.287 * 10 ** 5 / 1000
    T_air = 226.73
    rho_air = 0.442
    #   assume diameter inlet of 1m
    D_in = 1
    A_in = np.pi * D_in ** 2 / 2
    #   Interpolation of Ideal Gas Data (need research!!!)
    del_h = (230.02 - 219.97) / (230 - 226.73)
    del_s = (1.43557 - 1.391) / (230 - 220)
    #   the Dead State
    #   define the Dead State Pressure [kPa]
    P_0 = R_air * 10 ** 2
    #   define the Dead State Temperature [K]
    T_0 = T_2
    #   define the Dead State Specific Enthalpy [kJ/kg]
    h_0 = 230.02 + (226.73 - 230) * del_h
    #   define the Dead State Specific Entropy [kJ/kg]
    s_0 = 1.4355 + (226.73 - 230) * del_s
    #   define the Dead State Exergy [kJ/kg]
    Ex_0 = 0
     #   in order to perform design of experiments, the following arrays of design factors will be permuted.
    input_array = list(it.product(bpr, HPCR, LPCR, M, T_04))
    for i in range(len(input_array)):
        #   assign the new test case and key design parameters
        test_case = input_array[i]
        bpr = test_case[0]
        HPCR = test_case[1]
        LPCR = test_case[2]
        M = test_case[3]
        T_04 = test_case[4]

        #   Free Stream Velocity of air for the Mach Number
        v_air = M * a

        ###############################################################
        ###############################################################

        #   Evaluate energy flow at the entrance to fan[02]
        #   Need Presssure [kPa], Temperature [K], Enthalpy [kJ/kg], S.Exergy [kJ/kg], calc entropy generated, etc.

        P_02 = P_air * (1 + (k_air - 1) / 2 * M ** 2) ** (k_air / (k_air - 1))
        T_02 = T_2 * (1 + (k_air - 1) / 2  * M ** 2)
        h_02 = h_0 + cpa * (T_02 - T_ref)
        s_02 = s_0
        v_02 = M * a
        #   Exergy equation of state: Ex = h - h_0 - T_0 * (s - s_0)
        Ex_02 = h_02 - h_0 - T_0 *(s_02 - s_0) + (v_02) ** 2 / 2000 + g * z / 1000

        ###############################################################
        ###############################################################

        #   Evaluate the energy flow at the bypass duct [013]
        T_013 = T_02 * FPR ** ((k_air - 1) / (eta_pF * k_air))
        P_013 = P_02 * (T_013 / T_02) ** (k_air / (k_air - 1))
        h_013 = h_0 + cpa * (T_013 - T_ref)
        s_013 = s_02 + cpa * math.log(T_013 / T_02) - R_air * math.log(P_013 / P_02)
        s_gen_01302 = s_013 - s_02
        #   calculate the jet velocity of the bypass duct
        v_jet_b = np.sqrt(2 * cpa * eta_pF * (T_013 - T_02) * 1000) + v_air
        Ex_013 = h_013 - h_0 - T_0 * (s_013 - s_0) + (v_jet_b) ** 2 / 2000 + g * z / 1000
        X_des_01302 = T_0 * s_gen_01302

        ###############################################################
        ###############################################################

        #   Evaluate the energy flow at the entrance to the HPC [023]
        T_023 = T_02 * LPCR ** ((k_air - 1) / (eta_pC_LPS * k_air))
        P_023 = P_02 * (T_023 / T_02) ** (k_air / (k_air - 1))
        h_023 = h_0 + cpa * (T_023 - T_ref)
        s_023 = s_02 + cpa * math.log(T_023 / T_02) - R_air * math.log(P_023 / P_02)
        s_gen_02302 = s_023 - s_02
        Ex_023 = h_023 - h_0 - T_0 * (s_023 - s_0) + g * z / 1000
        X_des_02302 = T_0 * s_gen_02302

        #   Find K_LPS
        k_lps = (cpa / cpe) / T_04 * (2 * (T_023 - T_02))

        #   Mass flow through bypass duct
        m_4 = k_exhaust / (k_exhaust - 1) ** 0.5 * ((k_exhaust + 1) / 2) ** (- (k_exhaust + 1) / (2 * (k_exhaust - 1)))
        m_13 = k_air / (k_air - 1) ** 0.5 * ((k_air + 1) / 2) **(- (k_air + 1) / (2 * (k_air - 1)))
        A_13_4 = m_4 /m_13 * (cpa / cpe) ** 0.5 * HPCR * (T_013 / T_04) ** 0.5

        ###############################################################
        ###############################################################

        #   Evaluate the energy flow at the entrance to the Core [03]
        T_03 = T_023 * HPCR ** ((k_air - 1) / (eta_pC_HPS * k_air))
        P_03 = P_023 * (T_03 / T_023) ** (k_air / (k_air - 1))
        h_03 = h_0 + cpa * (T_03 - T_ref)
        s_03 = s_023 + cpe * math.log(T_03 / T_023) - R_air * math.log(P_03 / P_023)
        s_gen_03023 = s_03 - s_023
        Ex_03 = h_03 - h_0 - T_0 * (s_03 - s_0) + g * z / 1000
        X_des_03023= T_0 * s_gen_03023

        #   Find K_HPS
        k_hps = cpa / cpe * (T_03 / T_023 - 1) * T_023 / T_04

        ###############################################################
        ###############################################################

        #   Evaluate the energy flow at the exit of the Combustion Chamber [04]
        T_04 = T_04
        P_04 = P_03 * core_pressure_ratio
        h_04 = h_0 + cpe * (T_04 - T_ref)
        s_04 = s_03 + cpe * math.log(T_04 / T_03) - R_e * math.log(P_04 / P_03)
        s_gen_0403 = s_04 - s_03
        Ex_04 = h_04 - h_0 - T_0 * (s_04 - s_0) + g * z / 1000
        X_des_0403 = T_0 * s_gen_0403

        ###############################################################
        ###############################################################

        #Evaluate the energy flow at the exit of HPT [045]
        T_045 = T_04 * (1 - k_hps)
        P_045 = P_04 * (T_045 / T_04) ** (k_exhaust / (eta_pT_HPS * (k_exhaust - 1)))
        h_045 = h_0 + cpe * (T_045 - T_ref)
        s_045 = s_04 + cpe * math.log(T_045 / T_04) - R_e * math.log(P_045 / P_04)
        s_gen_04504 = s_045 - s_04
        Ex_045 = h_045 - h_0 - T_0 * (s_045 - s_0) + g * z / 1000
        X_des_04504 = T_0 * s_gen_04504
        A_4_45 = (T_045 / T_04) ** ((2 * k_exhaust - eta_pT_HPS *(k_exhaust - 1)) / (2 * eta_pT_HPS * (k_exhaust - 1)))

        ###############################################################
        ###############################################################

        #   Evaluate the energy flow at the exit of LPT [05]
        T_05 = T_045 - T_04 * k_lps
        A_45_9 = (T_05 / T_04) ** ((2 * k_exhaust - eta_pT_LPS * (k_exhaust - 1)) / (2 * eta_pT_LPS * (k_exhaust - 1)))
        P_05 = P_045 * (T_05 / T_045) ** (k_exhaust / (eta_pT_LPS * (k_exhaust - 1)))
        h_05 = h_0 + cpe * (T_05 - T_ref)
        s_05 = s_045 + cpe * math.log(T_05 / T_045) - R_e * math.log(P_05 / P_045)
        s_gen_05045 = s_05 - s_045
        Ex_05 = h_05 - h_0 - T_0 * (s_05 - s_0) + g * z / 1000
        X_des_05045 = T_0 * s_gen_05045

        ###############################################################
        ###############################################################

        #   Evaluate the energy flow at the exit [09]
        T_09 = T_05 * (1 - (1 - (P_02 / P_05) ** ((k_air - 1) / k_air)))
        P_09 = P_02
        h_09 = h_0 + cpe * (T_09 - T_ref)
        s_09 = s_05
        #   isentropic assumption -> s_gen=0 for nozzle
        s_gen_0905 = 0
        X_des_0905 = T_0 * s_gen_0905

        #   calculate the jet velocity of the core exhaust
        v_jet_c = np.sqrt(2 * cpa * (T_05 - T_09) * 1000)
        Ex_09 = h_09 - h_0 - T_0 * (s_09 - s_0) + v_jet_c ** 2 / 2000 + g * z / 1000

        F_n_iter = (1 / (bpr + 1)) * v_jet_c  + (bpr / (bpr + 1)) * v_jet_b - v_air
        X_des_iter = X_des_0905 + X_des_05045 + X_des_04504 + X_des_0403 + X_des_03023 + X_des_02302 + X_des_01302
        #	appending the specific thrust, exergy destroyed etc arrays each iteration to build the vectors for regression analysis
        F_n.append(F_n_iter)
        X_des.append(X_des_iter)
        bpr_r.append(bpr)
        HPCR_r.append(HPCR)
        LPCR_r.append(LPCR)
        M_r.append(M)
        T_04_r.append(T_04)

        if i == 99999:
            #station labels list and exergy list for plotting
            stations1= ["Ex_02", "Ex_013", "Ex_023", "Ex_03", "Ex_04", "Ex_045", "Ex_05", "Ex_09"]
            exergy = [Ex_02, Ex_013, Ex_023, Ex_03, Ex_04, Ex_045, Ex_05, Ex_09]
            #	station labels list and exergy destroyed list for plottting
            stations2 = ["Dead State", "X_des_01302", "X_des_02302", "X_des_03023", "X_des_0403", "X_des_04504", "X_des_05045", "X_des_0905"]
            exergy_des = [0, X_des_01302, X_des_02302, X_des_03023, X_des_0403, X_des_04504, X_des_05045, X_des_0905]
            print(exergy_des)
            #	begin plotting
            plt.figure(1)
            plt.grid(True)
            plt.title("The Exergy at each Station")
            plt.xlabel("Station")
            plt.ylabel(r"$\chi$  (kJ/kg)")
            plt.bar(range(len(exergy)), exergy, width = 4/len(exergy), color = "red", tick_label = stations1, align = "center")
            plt.figure(2)
            plt.grid(True)
            plt.title("Exergy Destroyed")
            plt.xlabel("Station")
            plt.ylabel(r"$\chi_{des}$")
            plt.bar(range(len(exergy_des)), exergy_des, width = (4)/len(exergy_des), tick_label = stations2, align = "center")
            plt.show()
    return F_n, X_des, bpr_r, HPCR_r, LPCR_r, M_r, T_04_r
stage_analysis()
