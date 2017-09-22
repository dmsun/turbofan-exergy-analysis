#! usr/bin/env python3
# this script will calculate the years to retire with respect to the savings ratio
from decimal import Decimal
import numpy as np
import matplotlib.pyplot as plt
from calc_super_contrib import calc_super_contrib
from calc_taxable_income import calc_taxable_income
from calc_tax import calc_tax

def years_to_retire(g, w, gross_income, savings_ratio, super_rate, extra_super):
	years_req = []
	""" The principal required is the amount of capital to reach a withdraw rate that is 
	equal to your annual expenditure"""
	annual_taxable_income = calc_taxable_income(gross_income,super_rate + extra_super)
	annual_net_income = float(annual_taxable_income - calc_tax(annual_taxable_income))
	
	for i in range(len(savings_ratio)):
		annual_savings = savings_ratio[i]*annual_net_income
		annual_expenditure = annual_net_income - annual_savings		
		principal_required = annual_expenditure / w
		savings = 0
		years = 0
		
		while savings < principal_required and years < len(savings_ratio) :
			savings += annual_savings + (g * savings)
			#	inflations is assumed to be 0.03
			principal_required += principal_required * 0.03
			years += 1
		years_req.append(years)
	return years_req
	
def net_worth(growth, withdraw, savings, gross_income, savings_ratio, age, current_year, super_rate, extra_super):
	net_worth_array = []
	year = []

	years_retire = years_to_retire(growth, withdraw, gross_income, savings_ratio, super_rate, extra_super) 

	annual_taxable_income = calc_taxable_income(gross_income,super_rate + extra_super)
	annual_net_income = float(annual_taxable_income - calc_tax(annual_taxable_income))
	annual_savings = savings_ratio * annual_net_income
	annual_super = float(calc_super_contrib(gross_income, super_rate + extra_super, employer_co_contribution))
	
	for i in range(max(years_retire)):
		net_worth_row = []
		net_worth = savings
		year.append(current_year + i)
		for j in range(max(years_retire)):
			net_worth += net_worth * growth + annual_savings[i] + annual_super
			net_worth_row.append(net_worth)
		net_worth_array.append(net_worth_row)
	return net_worth_array, year

#	assumptions
growth_rate = 0.07
inflation_rate = 0.03
gross_income = 65000
super_rate = 0.095
extra_super = 0.03
employer_co_contribution = 0.03
savings = 15000
#	number of intervals or interations
n = 25

#SF = float(input("What safety factor would you like? Enter a decimal number 0 < SF <= 1. ->"  ))
SF = 1
withdraw_rate = round(SF * (growth_rate - inflation_rate),4)

#	The safety factor describes the proportion of your total investments you would like to live on.
#	A SF of 1 would mean your withdraw rate is exactly equal to the difference of the growth rate of 
#	your investments and inflation (minimal sustainability) and the closer this number is to 0 the more 
#	sustainable it is as you have more buffer room between fluctuations in the natural inflation rate 
#	and growth rate.

# few setup calculations
savings_rate = np.linspace(0.2, 1, num = n)
x1 = savings_rate	

#	years_to_retire(g, w, gross_income, savings_ratio, super_rate, extra_super):
y1 = years_to_retire(growth_rate, withdraw_rate, gross_income, savings_rate, super_rate, extra_super)
baseline = np.linspace(n, n, num = n)

#	net_worth(growth, withdraw, savings, gross_income, savings_ratio, age, current_year, super_rate, extra_super):
net_value, year = net_worth(growth_rate, withdraw_rate, savings, gross_income, savings_rate, 26, 2016, super_rate, extra_super)

plt.figure(1)
plt.subplot(211)
plt.plot(x1, y1, 'b', x1, baseline, 'r-') 
plt.axhline(y = n,color = "red")
plt.title("The Relationship between Savings Ratio and Years to FI")
plt.xlabel("Savings Ratio")
plt.ylabel("Years")
plt.axis([min(x1) - (max(x1)-min(x1))/n, max(x1) + (max(x1)-min(x1))/n, 0, n + 1])
plt.grid(True)

plt.subplot(212)

plt.grid(True)
plt.bar(x1,y1,width = (max(x1)-min(x1))/n ,color = "green")
plt.axhline(y = n,color = "red")
plt.axis([min(x1) - (max(x1)-min(x1))/n, max(x1) + (max(x1)-min(x1))/n, 0, n + 1])

plt.figure(2)
no_plots = n
plt.subplot()
plt.title("Net Worth over time for difference savings rates")
plt.xlabel("Year")
plt.ylabel("Net Worth in $")
plt.axvline(x = 2016 + n-1, color = "red")
plt.axhline(y = 1000000, color = "red")
for i in range(no_plots):
	plt.plot(year, net_value[i * int(n/no_plots)], label = "Savings Rate = {}".format(round(savings_rate[i * int(n/no_plots)],2)))
plt.legend(bbox_to_anchor=(0, 1), loc=2, borderaxespad=0.)
plt.show()

