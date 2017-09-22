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

def render_mpl_table(data, col_width=3.0, row_height=0.625, font_size=8,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0,
                     ax=None, **kwargs):
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')

    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)

    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in  six.iteritems(mpl_table._cells):
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0]%len(row_colors) ])
    return ax
# 	Year to Date accumsum
#	creates a pdf file and assigns it to pdf. Each of the following actions are written to the pdf.
#	At the end of the instructions the pdf is closed.
def ytd (df_work, cwd, tableau20):

    # some local variables
    today = dt.date.today()
    unique_years = list(df_work.Fin_year.unique())

    for fin_year in unique_years:
        year = fin_year[:7]
        year = year[-4:]
        year = int(year)
        begin = dt.date(year, 7, 1)
        if year == today.year:
            date_diff = today - begin
        else:
            date_diff = dt.date(year + 1, 7, 1) - begin
        #print(fin_year)
        df_year = df_work.loc[df_work.Fin_year == fin_year, :]
        df_ytd_work = df_year.loc[:,('Date','Cost')].groupby('Date', as_index = False).sum().sort_values('Date', ascending = True)
        df_ytd_work.loc[:, 'Running Total'] = df_ytd_work.loc[:, 'Cost'].cumsum()
        df_cat = df_year.loc[:,('Category', 'Cost')].groupby('Category', as_index = False).sum().sort_values('Cost', ascending = False)
        df_cat = df_cat.round(decimals = 2)
        df_cat = df_cat.reset_index(drop = True)

        #calc some local variables
        ytd_spend = round(df_ytd_work['Running Total'].iloc[-1], 2)
        average_spend = round(ytd_spend / date_diff.days, 2)
        #print(date_diff)
        max_cat = df_cat.loc[:, 'Cost'].max()
        last_day = df_ytd_work.Date.iloc[-1]
        #print checks
        print("The total spend in Fin_year {0} is ${1}".format(fin_year, ytd_spend))
        #print("The average daily spend is $", average_spend)

        with PdfPages("{0}\\reports\\{1} YTD Expense Report.pdf".format(cwd, fin_year)) as pdf:

            fig, ax = plt.subplots()
            plt.title("Spend totals for {}".format(fin_year))
            ax.stackplot(list(df_ytd_work.Date), df_ytd_work['Running Total'], color = tableau20)
            ax.set_ylabel("Cost")
            ax.set_xlim([df_ytd_work.Date[0], last_day])
            ax.set_ylim([0, ytd_spend])
            plt.tick_params(axis='both', which='major', labelsize=8)
            plt.tick_params(axis='both', which='minor', labelsize=8)
            ax.annotate("Total Spend is ${}".format(ytd_spend), xy = [last_day, ytd_spend], xytext = [0.5, 0.9*ytd_spend], textcoords ='data')
            labels = ax.get_xticklabels()
            plt.setp(labels, rotation=30, fontsize=8)
            plt.tight_layout()
            pdf.savefig(fig)
            plt.close()

            fig, ax = plt.subplots()
            df_cat.loc[:,['Category', 'Cost']].plot.bar(subplots = True, ax = ax, x = 'Category', y = 'Cost', legend = False, color = tableau20)
            ax.set_ylabel("Total Spend per Category")
            ax.set_ylim([0, max_cat])
            ax.set_title("")
            labels = ax.get_xticklabels()
            plt.setp(labels, rotation=90, fontsize=6)
            plt.tight_layout()
            pdf.savefig(fig)
            plt.close()

            fig, ax = plt.subplots()
            render_mpl_table(df_cat, header_columns=0, col_width=2.0, row_height=0.7, font_size=8, ax= ax)
            ax.axis('off')
            pdf.savefig(fig)
            plt.close
