#! usr/bin/env python3

#	import modules from main
import os
import math
import decimal
import datetime as dt
import calendar

#	import other modules
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

#	some initial setup - abbreviating the Decimal command, changing the style of matplotlib, assigning the current working directory variable and filepath variable

def networth(cwd, tableau20):
    filepath = "{}\\data\\Life - Networth.csv".format(cwd)
    columns = ['Month',
               'Net Worth',
               'Growth',
               'Delta',
               'Car',
               'ING Savings',
               'UBank Savings',
               'Savings',
               'Superannuation',
               'Acorns',
               'Stocks',
               'Cryptocurrency',
               'Assets Subtotal',
               'HELP Debt',
               'Car Debt',
               'Personal Debt',
               'Credit Debt',
               'Liabilities Total']
    df_networth = pd.read_csv(filepath,
                              header = 0,
                              #names = columns,
                              parse_dates = [0],
                              infer_datetime_format = True,
                              dayfirst = True)
    df_networth.drop(['ING Savings', 'UBank Savings'], axis = 1)
    df_networth = df_networth.dropna()
    for (col, colname) in enumerate(columns):
        col_len = len(df_networth[colname])
        try:
            for row in range(col_len):
                if '$' in df_networth.iloc[row, col] or '%' in df_networth.iloc[row, col]:
                    df_networth.loc[:, colname] = (df_networth.loc[:, colname].str.replace(r'[^-+\d.]', '').astype(float))
        except:
            continue
    with PdfPages("{}\\Reports\\Net Worth.pdf".format(cwd)) as pdf:
        fig, ax = plt.subplots()
        df_networth.plot(kind = 'line', subplots = True, ax = ax, x = 'Month', y = 'Net Worth', color = tableau20[1])
        df_networth.plot(kind = 'line', subplots = True, ax = ax, x = 'Month', y = 'Assets Subtotal', color = tableau20[3])
        df_networth.plot(kind = 'line', subplots = True, ax = ax, x = 'Month', y = 'Liabilities Total', color = tableau20[4])
        #max_cat = max(list(df_qtr_cat_pivot.max()))
        ax.set_xlabel("Month")
        ax.set_ylabel("Value")
        #ax.set_ylim([0, max_cat])
        ax.set_title("Net Worth over time")
        labels = ax.get_xticklabels()
        plt.setp(labels, rotation=90, fontsize=6)
        ax.xaxis.set_label_position('bottom')
        x = list(df_networth['Month'].get_values())
        y = list(np.zeros(len(df_networth['Net Worth'])))
        ax = plt.plot(x, y, color = 'black')
        #plt.legend(labels= ['Q{}'.format(qtr) for qtr in list(df_qtr_cat_pivot)])
        plt.tight_layout()
        pdf.savefig(fig)
        plt.close()

        fig, ax = plt.subplots()
        df_networth.plot(kind = 'line', subplots = True, ax = ax, x = 'Month', y = 'Acorns', color = tableau20[0])
        df_networth.plot(kind = 'line', subplots = True, ax = ax, x = 'Month', y = 'Stocks', color = tableau20[1])
        #max_cat = max(list(df_qtr_cat_pivot.max()))
        ax.set_xlabel("Month")
        ax.set_ylabel("Value")
        #ax.set_ylim([0, max_cat])
        ax.set_title("Net Worth over time")
        labels = ax.get_xticklabels()
        plt.setp(labels, rotation=90, fontsize=6)
        ax.xaxis.set_label_position('bottom')
        #plt.legend(labels= ['Q{}'.format(qtr) for qtr in list(df_qtr_cat_pivot)])
        plt.tight_layout()
        pdf.savefig(fig)
        plt.close()
