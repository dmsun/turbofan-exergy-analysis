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

"""
	The Aus_Qtrly reporting is used in order to collect neighbouring months to more easily compare
	the changes in expenditure for the corresponding months. This section of
"""

def qtr(df_work, cwd, tableau20):

    today = dt.date.today()
    begin = dt.date(2016,6,1)
    date_diff = today - begin
    unique_years = list(df_work.Fin_year.unique())


    for fin_year in unique_years:
        year = fin_year[:7]
        year = year[-4:]
        year = int(year)
        #	subset the dataframe for current year
        df_year_work = df_work.loc[(df_work.Fin_year == fin_year), ('Date', 'Month', 'Aus_Qtr', 'Cost', 'Category')]
        df_qtr_sum = df_year_work.loc[:, ('Aus_Qtr', 'Cost', 'Category')].groupby(['Aus_Qtr','Category'], as_index = False).sum()
        unique_qtrs = list(df_year_work.Aus_Qtr.unique())
        max_qtr = df_qtr_sum.Cost.max()

        with PdfPages("{0}\\Reports\\{1} Aus_Qtrly Reports.pdf".format(cwd, fin_year)) as pdf:
            df_qtr_cat_pivot = pd.pivot_table(df_qtr_sum, values = 'Cost', index = ['Category'], columns = ['Aus_Qtr'], aggfunc = np.sum).fillna(value=0)
            fig, ax = plt.subplots()
            df_qtr_cat_pivot.plot.bar(subplots = False, ax= ax, legend = True, color=tableau20)
            max_cat = max(list(df_qtr_cat_pivot.max()))
            ax.set_xlabel("Category")
            ax.xaxis.set_label_position('bottom')
            ax.set_ylabel("Spend")
            ax.set_ylim([0, max_cat])
            ax.set_title("Spending by Aus_Qtr {}".format(year))
            labels = ax.get_xticklabels()
            plt.setp(labels, rotation=90, fontsize=6)
            plt.legend(labels= ['Q{}'.format(qtr) for qtr in list(df_qtr_cat_pivot)])
            plt.tight_layout()
            pdf.savefig(fig)
            plt.close()

            for qtr in unique_qtrs:
                #	select the months for the first Aus_Qtr (January - March)
                df_qtr_work = df_year_work.loc[(df_work.Aus_Qtr == qtr), :]
                df_qtr_by_mon = df_qtr_work.loc[:, ('Month', 'Cost', 'Category')].groupby(('Month','Category'), as_index = False).sum()
                qtr_pivot = pd.pivot_table(df_qtr_work, values = 'Cost', index = ['Category'], columns = ['Month'], aggfunc = np.sum).fillna(value=0)
                fig, ax = plt.subplots()
                qtr_pivot.plot.bar(subplots = False, ax= ax, legend = True, color=tableau20)
                max_cat = df_qtr_by_mon.Cost.max()
                ax.set_xlabel("Category")
                ax.xaxis.set_label_position('bottom')
                ax.set_ylabel("Spend")
                ax.set_ylim([0, max_cat])
                ax.set_title("Spending for Q{0} {1}".format(qtr, year))
                labels = ax.get_xticklabels()
                plt.setp(labels, rotation=90, fontsize=6)
                plt.legend(labels= [calendar.month_abbr[mon] for mon in list(qtr_pivot)])
                plt.tight_layout()
                pdf.savefig(fig)
                plt.close()
