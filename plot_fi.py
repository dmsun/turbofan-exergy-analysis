def plot_fi(retirement_age, age,, principal, expenses,  networth, r_income):
    I = retirement_age - age
    fig, ax1 = plt.subplots()
    P = np.linspace(float(principal), float(principal), num= len(I))
    exp = np.linspace(float(expenses), float(expenses), num = len(I))
    Networth = ax1.plot(I, networth, 'b', label = 'Networth')
    Principal = ax1.plot(I, P, 'k--', label = 'Principal Required')
    ax1.set_ylabel('Prinicipal Required in $', color='k')
    plt.legend(loc=2)
    ax2 = ax1.twinx()
    R_income = ax2.plot(I, r_income, 'g', label = 'Retirement Income')
    Exp = ax2.plot(I, exp, 'r--', label = 'Annual Expenses')
    ax2.set_ylabel('Retirement Income in $', color='k')
    plt.legend(loc=4)
    plt.show()