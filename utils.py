#! usr/bin/env python3

from decimal import Decimal as D
import calendar
import datetime as dt
import six

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd


"""This script will compile several useful calculators that will be used in other parts of the financial independence calculator

In the long term, the average annual rate of return of a diversified security portfolio is assumed to be 7%. The safety_rate is a factor used to account for variations of this growth through the short term"""
#	These are the "Tableau 20" colors as RGB.
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

#	Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)

def withdraw_rate(growth_rate = 0.07, inflation_rate = 0.03, safety_factor = 1):
    """ The withdraw rate is the rate at which you can "safely" withdraw upon your investments and expect to have a steady income for the duration of your life. The safety factor determines how conservative the approach is. By default, the SF is 1 which is the most aggressive appraoch. Value must be greater than 0
    """
    """while True:
        try:
            value = int(safety_factor)
        except:
            print("Please enter the safety factor such that 0 < SF <= 1")
            continue
        if 0 < safety_factor <= 1:
            break
        else:
            print("Please enter the safety factor such that 0 < SF <= 1")"""
    return D(safety_factor * (growth_rate - inflation_rate))

def principal(expenses, withdraw_rate):
    """ The principal required is proportional to average annual expenditure
    and inversely proportional to the withdrawal rate.

    Note: this does not include any additional investments you would like to have in the future. It's your current situation as it exists now."""
    principal = D(round(expenses / withdraw_rate,2))
    return principal

def super(gross_income, super_rate = 9.5, co_contribution = 0):
    super = D(round((super_rate + co_contribution) / 100 * gross_income,2))
    return super

def taxable_income(gross_income, super_rate = 9.5, co_contribution = 0):
    taxable_income = D(round((1 - (super_rate + co_contribution) / 100) * gross_income,2))
    return taxable_income

def tax(taxable_income):
    """ Tax Brackets: 2017-2018
    $0 - $18 200            NIL
    $18 201 - $37 000       $0.19 for every $1 over $18 200
    $37 001 - $87 000       $3 572 plus $0.325 for every $1 over $37 000
    $87 001 - $180 000      $19 882 plus $0.37 for every $1 over $87 000
    $180 001 and over       $54 547 plus $0.45 for every $1 over $180 000
    """
    if taxable_income >= 180001:
        tax = D(round(54232 + D(0.45) * (taxable_income - 180000),2))
    elif 87001 <= taxable_income <= 180000:
        tax = D(round(19882 + D(0.37) * (taxable_income - 87000),2))
    elif 37001 <= taxable_income <= 87000:
        tax = D(round(3572 + D(0.325) * (taxable_income - 37000),2))
    elif 18201 <= taxable_income <= 37000:
        tax = D(round(D(0.19) * (taxable_income - 18000),2))
    elif 0 <= taxable_income <= 18200:
        tax = 0
    return tax

def compound(P, r, n, d, i):
    """ The compound interest formula with periodical deposits is adjusted with inflation to always provide todays money.
    """
    FV = (P * (1 + D(r/12)) ** n + d * ((1 + D(r/12)) ** n - 1)/ D(r/12) * (1 + D(r/12))) / (1 + D(i/12)) ** n
    FV = D(round(FV,2))
    return FV

def compound_array(P, r, n, d, i):
    """ The compound interest formula with periodical deposits is adjusted with inflation to always provide todays money.

    This function takes arrays for n - number of years/compound periods, uses the Decimal data type to ensure numerical precision.

    This code could be vectorised
    """

    FV = np.zeros(len(n))
    for k in range(len(n)):
        t = D(n[k])
        FV[k] = (P * (1 + r/12) ** t + d * ((1 + r/12) ** t - 1)/ (r/12) * (1 + r/12)) / (1 + i/12) ** t
    FV = np.around(FV,2)
    return FV

def stampduty(house_price):
    """Value of property    Rate of duty
    $0 - $14 000            $1.25 for every $100
    $14 001 - $30 000       $175 plus $1.50 for every $100
    $30 001 - $80 000       $415 plus $1.75 for every $100
    $80 001 - $300 000      $1 290 plus $3.50 for every $100
    $300 001 - $1 000 000   $8 990 plus $4.50 for every $100
    $1 000 001 - $3 000 000 $40 490 plus $5.50 for every $100
    > $3m	                $150 490 plus $7.00 for every $100
    """
    if 0 <= house_price <= 14000:
        stampduty = 1.25 * house_price / 100
    elif 14001 <= house_price <= 30000:
        stampduty = 175 + 1.5 * (house_price - 14000) / 100
    elif 30001 <= house_price <= 80000:
        stampduty = 415 + 1.75 * (house_price - 30000)/ 100
    elif 80001 <= house_price <= 300000:
        stampduty = 1290 + 3.50 * (house_price - 80000) / 100
    elif 300001 <= house_price <= 1000000:
        stampduty = 8990 + 4.50 * (house_price - 300000)/ 100
    elif 1000001 <= house_price <= 3000000:
        stampduty = 40490 + 5.50 * (house_price - 1000000) / 100
    elif house_price > 3000000:
        stampduty = 150490 + 7.00 * (house_price - 3000000) / 100
    return stampduty


def plot_fi(ageVec, networthVec,superVec, savingsVec, principalVec, incomeVec, expensesVec, index_fi):
    fig, ax1 = plt.subplots()
    networth = ax1.plot(ageVec, networthVec, 'b', label = 'Networth')
    super = ax1.plot(ageVec, superVec, 'c', label = 'Super')
    savings = ax1.plot(ageVec, savingsVec, 'g', label = 'Savings')
    principal = ax1.plot(ageVec, principalVec, 'k--', label = 'Principal Required')
    ax1.set_ylabel('Prinicipal Required in $', color='k')
    plt.legend(loc=2)

    # create a separate axis on the same graph, plot income v age, expenses vs age. Expenses is a horizontal line. Label this axis as Retirement income
    ax2 = ax1.twinx()
    retirement_income = ax2.plot(ageVec, incomeVec, 'm', label = 'Retirement Income')
    annual_expenses = ax2.plot(ageVec, expensesVec, 'r--', label = 'Annual Expenses')
    ax2.set_ylabel('Retirement Income in $', color='k')

    # plots vertical line at the age of finanical independence which is parsed into the function. This is dependent of calculations prior to calling the function
    plt.axvline(x=ageVec[index_fi], label = "Finanical Indepdence")
    plt.legend(loc=4)

    plt.show()

def quarter_aus(quarter):
    """
    Maps quarters of the calendar year to the quarter in the Australian Financial Year
    """
    if quarter == 2:
        quarter_aus = 4
    else:
        quarter_aus = (quarter + 2) % 4
    return quarter_aus

def fin_year(date):
    """
    Maps the date to the corresponding financial year in Australia
    """
    if date.month < 7:
        fin_year = 'JUL' + str((date.to_pydatetime()).year - 1) + '-' + 'JUN' + str((date.to_pydatetime()).year)
    else:
        fin_year = 'JUL' + str((date.to_pydatetime()).year) + '-' + 'JUN' + str((date.to_pydatetime()).year + 1)
    return fin_year

#source for below table printing code
#https://stackoverflow.com/questions/26678467/export-a-pandas-dataframe-as-a-table-image
def render_mpl_table(data, col_width=3.0, row_height=0.625, font_size=14,
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

def mon_func(df_work, cwd, colours = tableau20):
    df_sub = df_work[['Date', 'Year', 'Month', 'Category', 'Cost']].sort_values(by = 'Date', ascending = True)
    df_mon = df_sub.groupby(by = ['Year', 'Month', 'Category']).agg({'Cost': np.sum}).reset_index()
    df_mon.sort_values(by = ['Year', 'Month','Cost'], ascending = False, inplace = True)
    df_mon = df_mon.round(decimals = 2)
    df_day = df_sub.groupby(by = ['Year', 'Month', 'Date']).agg({'Cost': np.sum}).reset_index()
    df_day.loc[:,'Running Total'] =  df_day.groupby(by = ['Year', 'Month'])['Cost'].cumsum()

    for name, group in df_day.groupby(by = ['Year', 'Month']):
        with PdfPages("{0}\\reports\\{3}.{1} Expense Report - {2}.pdf".format(cwd, name[1], calendar.month_name[name[1]], name[0])) as pdf:
            # write to the pdf on a new page and close the plot. closing maybe redundant - need to perform some testing.
            pdf.savefig(month_day_report(name, group, tableau20))
            plt.close()
            pdf.savefig(cat_report(df_mon.loc[(df_mon.Month == name[1]), ('Category', 'Cost')], name))
            plt.close()
            pdf.savefig(report_table(df_mon.loc[(df_mon.Month == name[1]), ('Category', 'Cost')], name))
            plt.close()

def qtr_func(df_work, cwd, colours = tableau20):
    df_sub = df_work[['Date', 'Fin_Year', 'Year', 'Aus_Qtr', 'Month', 'Category', 'Cost']].sort_values(by = 'Date', ascending = True)

    for name, group in df_sub.groupby(by = ['Fin_Year']):
        group_pivot = pd.pivot_table(group.groupby(by = ['Fin_Year', 'Aus_Qtr', 'Category']).agg({'Cost': np.sum}).reset_index(), values = 'Cost', index = 'Category', columns = 'Aus_Qtr', aggfunc='sum', fill_value=0)

        with PdfPages("{0}\\Reports\\{1} Aus_Qtrly Reports.pdf".format(cwd, name)) as pdf:
            fig, ax = plt.subplots()
            group_pivot.plot.bar(subplots = False, ax= ax, legend = True, color=tableau20)
            ax.set_xlabel("Category")
            ax.xaxis.set_label_position('bottom')
            ax.set_title("Spending by Quarter {}".format(name))
            labels = ax.get_xticklabels()
            plt.setp(labels, rotation=90, fontsize=6)
            plt.legend(labels= ['Q{}'.format(qtr) for qtr in list(group_pivot)])
            plt.tight_layout()
            pdf.savefig()
            plt.close()

            for qtr, df_qtr in group[group.Fin_Year == name].groupby(by = 'Aus_Qtr'):
                fig, ax = plt.subplots()
                qtr_pivot = pd.pivot_table(df_qtr, values = 'Cost', index = 'Category', columns = 'Month', aggfunc='sum', fill_value=0)
                qtr_pivot.plot.bar(subplots = False, ax= ax, legend = True, color=tableau20)
                ax.set_xlabel("Category")
                ax.xaxis.set_label_position('bottom')
                ax.set_ylabel("Spend")
                ax.set_title("Spending for Q{0} {1}".format(qtr, name))
                labels = ax.get_xticklabels()
                plt.setp(labels, rotation=90, fontsize=6)
                plt.legend(labels= [calendar.month_abbr[mon] for mon in list(qtr_pivot)])
                pdf.savefig(fig)
                plt.close()

def year_func(df_work, cwd, colours = tableau20):
    df_sub = df_work[['Date', 'Fin_Year', 'Year', 'Month', 'Category', 'Cost']].sort_values(by = 'Date', ascending = True)
    df_year = df_sub.groupby(by = ['Fin_Year', 'Category']).agg({'Cost': np.sum}).reset_index()
    df_year = df_year.round(decimals = 2)
    df_day = df_sub.groupby(by = ['Fin_Year', 'Date']).agg({'Cost': np.sum}).reset_index()
    df_day.loc[:,'Running Total'] =  df_day.groupby(by = ['Fin_Year'])['Cost'].cumsum()
    for name, group in df_day.groupby(by = ['Fin_Year']):
        with PdfPages("{0}\\reports\\{1} YTD Expense Report.pdf".format(cwd, name)) as pdf:
            # write to the pdf on a new page and close the plot. closing maybe redundant - need to perform some testing.
            pdf.savefig(year_day_report(name, group))
            plt.close()
            pdf.savefig(cat_report(df_year.loc[(df_year.Fin_Year == name)], name))
            plt.close()
            pdf.savefig(report_table(df_year.loc[(df_year.Fin_Year == name), ('Category', 'Cost')], name))
            plt.close()


def month_day_report(name, group, colours = tableau20):

        ax = group.plot(x = 'Date', y = 'Running Total', title = 'Total Spend for {0} - {1}'.format(calendar.month_name[name[1]], name[0]), color = colours[0])

        # set axis labels
        ax.set_xlabel("Day of Month")
        ax.xaxis.set_label_position('bottom')
        ax.set_ylabel("Cost")
        # check what this does
        plt.tick_params(axis='both', which='major', labelsize=8)
        plt.tick_params(axis='both', which='minor', labelsize=8)

        # define a variables to be used for scaling, setting limits on axes, etc.
        num_days = calendar.monthrange(name[0], name[1])[1]
        first_day = group['Date'].min()
        last_day = group['Date'].max()
        sum_expenses = group['Running Total'].max()
        del_time = dt.timedelta(days= num_days * 0.35)

        # set axis limits
        ax.set_xlim([group['Date'].min(), last_day])
        ax.set_ylim([0, sum_expenses])

        ax.annotate("Total Expenditure is ${}".format(round(sum_expenses,2)), xy = [last_day, sum_expenses], xytext = [first_day + del_time, 0.9*sum_expenses], textcoords ='data')
        ax.annotate("Average Expenditure is ${}".format(round(sum_expenses/num_days, 2)), xy = [last_day, sum_expenses], xytext = [first_day + del_time, 0.8*sum_expenses], textcoords ='data')
        labels = ax.get_xticklabels()
        plt.setp(labels, fontsize=8)
        plt.tight_layout()

def cat_report(df, name, colours = tableau20):
        fig, ax = plt.subplots()
        df.plot.bar(subplots = True, ax = ax, x = 'Category', y = 'Cost', legend = False, color = colours)
        ax.set_xlabel("Spend Category")
        ax.xaxis.set_label_position('top')
        ax.set_ylabel("Total Spend per Category")
        ax.set_title("")
        labels = ax.get_xticklabels()
        plt.setp(labels, rotation=90, fontsize=6)
        plt.tight_layout()

def report_table(df, name):
    fig, ax = plt.subplots()
    render_mpl_table(df, header_columns=0, col_width=2.0, row_height=0.7, font_size = 8, ax= ax)
    ax.axis('off')



def year_day_report(name, group, colours = tableau20):
            ax = group.plot(x = 'Date', y = 'Running Total', title = "Spend totals for {}".format(name), color = colours[0])
            ax.set_ylabel("Cost")

            # define a variables to be used for scaling, setting limits on axes, etc.
            first_day = group['Date'].min()
            last_day = group['Date'].max()
            sum_expenses = group['Running Total'].max()
            del_time = dt.timedelta(days= (last_day - first_day).days * 0.35)
            ax.set_xlim([first_day, last_day])
            ax.set_ylim([0, sum_expenses])

            plt.tick_params(axis='both', which='major', labelsize=8)
            plt.tick_params(axis='both', which='minor', labelsize=8)

            ax.annotate("Total Spend is ${}".format(round(sum_expenses, 2)), xy = [last_day, sum_expenses], xytext = [first_day + del_time, 0.9*sum_expenses], textcoords ='data')
            labels = ax.get_xticklabels()
            plt.setp(labels, rotation=30, fontsize=8)
            plt.tight_layout()
