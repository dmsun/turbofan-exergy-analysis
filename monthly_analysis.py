#! usr/bin/env python3

#	import modules from main
import os
import math
import decimal
import datetime as dt
import calendar
import six

#	import other modules
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

#	the below is a month by month analysis
def mon (df_work, cwd, tableau20):
    #   creating a list of the unique months and assigning that to the number of rows which will be called for month by month analysis
    #   limitation of this - month must be unique and may only work for 1 calendar year. I may be able to check this later.
    unique_years = list(df_work.Year.unique())
    for year in unique_years:
        df_year = df_work.loc[df_work.Year == year, :]
        unique_mons = list(df_year.Month.unique())
        for month in unique_mons:
        #	check for emptiness and break if required
            df_mon_exp = df_year.loc[(df_year.Month == month), :]
            #   begin the daily analysis
            #   Sort by Date
            df_mon_exp.sort_values(by = 'Date', ascending = True)

            #   find the total expenses for each month by category and assign to a new df
            df_cat = df_mon_exp.loc[:,('Category', 'Cost')].groupby('Category', as_index = False).sum().sort_values('Cost', ascending = False)
            df_cat = df_cat.round(decimals = 2)
            df_cat = df_cat.reset_index(drop = True)

            #   calculate MTD expenses.
            #   sum cost for each day, create an accumulating total column

            df_day_exp = df_mon_exp.loc[:,('Date', 'Cost')].groupby('Date').sum()
            df_day_exp.loc[:,'Running Total'] = df_day_exp.loc[:,'Cost'].cumsum()
            df_day_exp.index = df_day_exp.index.day
            df_day_exp = df_day_exp.round(decimals = 2)

            #   calculate some variables
            #   grabs last day of current month
            last_day = calendar.monthrange(year, month)[1]
            sum_expenses = df_day_exp.Cost.sum().round(decimals = 2)
            avg_daily_expense = round(sum_expenses/last_day, 2)
            max_cat = df_cat.loc[:, 'Cost'].max()

            #print("The average daily expense for {0} {1} was ${2}".format(calendar.month_name[month], year, avg_daily_expense))
            #print("The total spend for {0} {1} was ${2}".format(calendar.month_name[month], year, sum_expenses))

            #  creates a pdf file. Each of the following actions are written to the pdf. At the end of the instructions the pdf is closed.
            with PdfPages("{0}\\reports\\{3}.{1} Expense Report - {2}.pdf".format(cwd, month, calendar.month_name[month], year)) as pdf:

                fig, ax = plt.subplots()
                plt.title("Accumulating totals for {0} - {1}".format(calendar.month_name[month], year))
                ax.stackplot(df_day_exp.index, df_day_exp['Running Total'], color=tableau20)
                #   set axis labels
                ax.set_xlabel("Day of Month")
                ax.xaxis.set_label_position('bottom')
                ax.set_ylabel("Cost")
                #   check what this does
                plt.tick_params(axis='both', which='major', labelsize=8)
                plt.tick_params(axis='both', which='minor', labelsize=8)
                #   set axis limits
                ax.set_xlim([1, last_day])
                ax.set_ylim([0, sum_expenses])
                #   include text that describes the total monthly expenditure
                ax.annotate("Total Expenditure is ${}".format(sum_expenses), xy = [last_day, sum_expenses], xytext = [0.35*last_day, 0.9*sum_expenses], textcoords ='data')
                ax.annotate("Average Expenditure is ${}".format(avg_daily_expense), xy = [last_day, sum_expenses], xytext = [0.35*last_day, 0.8*sum_expenses], textcoords ='data')
                labels = ax.get_xticklabels()
                plt.setp(labels, rotation=30, fontsize=8)
                plt.tight_layout()
                #   write to the pdf on a new page and close the plot. closing maybe redundant - need to perform some testing.
                pdf.savefig(fig)
                plt.close()

                fig, ax = plt.subplots()
                df_cat.loc[:, ('Category', 'Cost')].plot.bar(subplots = True, ax = ax, x = 'Category', y = 'Cost', legend = False, color=tableau20)
                ax.set_xlabel("Spend Category")
                ax.xaxis.set_label_position('top')
                ax.set_ylabel("Total Spend per Category")
                ax.set_ylim([0, max_cat])
                ax.set_title("")
                labels = ax.get_xticklabels()
                plt.setp(labels, rotation=90, fontsize=6)
                plt.tight_layout()
                pdf.savefig(fig)
                plt.close()

                fig, ax = plt.subplots()
                render_mpl_table(df_cat, header_columns=0, col_width=2.0, row_height=0.7, ax= ax)
                ax.axis('off')
                pdf.savefig(fig)
                plt.close
