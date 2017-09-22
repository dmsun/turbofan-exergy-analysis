import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import calendar
import datetime as dt
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

def mon_func(df_work, cwd):
    df_sub = df_work[['Date', 'Year', 'Month', 'Category', 'Cost']].sort_values(by = 'Date', ascending = True)
    df_mon = df_sub.groupby(by = ['Year', 'Month', 'Category']).agg({'Cost': np.sum}).reset_index()
    df_mon.sort_values(by = ['Year', 'Month','Cost'], ascending = False, inplace = True)
    df_day = df_sub.groupby(by = ['Year', 'Month', 'Date']).agg({'Cost': np.sum}).reset_index()
    df_day.loc[:,'Running Total'] =  df_day.groupby(by = ['Year', 'Month'])['Cost'].cumsum()

    for name, group in df_day.groupby(by = ['Year', 'Month']):
        utils.plot_mon(name, group)

    plt.show()
