"""
Assignment 3
Date:    5th March 2021
Course:  Applied Programming Lab(EE2703)
Faculty: Prof. Harishankar Ramachandhran

Submission by: Santosh G(EE19B055)

To complie and execute: python3 EE2703_ASSIGN3_EE19B055.py

PS: Run the code "generate_data.py" atleast once before running this code, as this program needs the data.
"""
# Importing necessary libraries
from pylab import *
from scipy import special as sp
import sys


try:
    data = np.loadtxt("fitting.dat", usecols=(1,2,3,4,5,6,7,8,9))
except OSError:
    sys.exit('File "fitting.dat" not found! Please Check\nRun the code in generate_data.py to create the file')
# Creating list of columns
DataCol = [[],[],[],[],[],[],[],[],[]]
# Extracting data as columns from the raw data
for i in range(len(data)):
    for j in range(len(data[i])):
        DataCol[j].append(data[i][j])

# Part 3
t = linspace(0,10,101)
sigma = logspace(-1,-3,9)
# Rounding off to 3 decimal places
sigma = around(sigma,3)

# Starting new figure/plot
figure(0)
for i in range(len(DataCol)):
    # Plotting the data in file
    plot(t,DataCol[i],label='$\sigma_{} = {}$'.format(i, sigma[i]))

# Part 4
# Defining the vectorized form of the fitting function
def g_t(t, A, B):
    return A*sp.jn(2,t) + B*t
A = 1.05
B = -0.105
trueFun = g_t(t, A, B)
# Plotting
plot(t, trueFun, label='true value', color='#000000')
xlabel('$t$')
ylabel('$f(t)+n(t)$')
title('Noisy plots vs True plot')
legend()
grid()
plt.savefig('Figure0.png')
show()

# Part 5
# Plotting a new diagram
figure(1)
xlabel('$t$')
ylabel('$f(t)$')
title('Errorbar Plot')
plot(t, trueFun, label='f(t)', color='#000000')
# Making errorbar plot
errorbar(t[::5], DataCol[0][::5], 0.1, fmt='ro', label='Error Bar')  #Collecting data in the intervals of 5, to increase readability
legend()
grid()
plt.savefig('Figure1.png')
show()


# Part 6
# Creating column vector for peforming least-squares estimation
jCol = sp.jn(2,t)
M = c_[jCol, t]
p = array([A, B])
# Creating matrix out of the column vectors
actual = c_[t,trueFun]

# Part 7
# Calculating the error in fit for various combinations of A and B
A = arange(0,2,0.1)
B = arange(-0.2,0,0.01)
epsilon = zeros((len(A), len(B)))
for i in range(len(A)):
    for j in range(len(B)):
            epsilon[i][j] = mean(square(DataCol[0][:] - g_t(t[:], A[i], B[j])))

# Part 8
# Plotting a new diagram
figure(2)
# Contour plot of epsilon with A and B on axes
contPlot=contour(A,B,epsilon,levels=10)
xlabel("A")
ylabel("B")
title("Contours of $\epsilon_{ij}$")
clabel(contPlot, inline=1, fontsize=10)
# Annotating the graph with exact location of minima
plot([1.05], [-0.105], 'ro')
grid()
annotate("Location\nof Minima", (1.05, -0.105), xytext=(-50, -40), textcoords="offset points", arrowprops={"arrowstyle": "->"})
plt.savefig('Figure2.png')
show()
# Part 9
# Least squares estimation
p, *rest = lstsq(M,trueFun,rcond=None)

#Part 10
#Plotting a new diagram
figure(3)
perr=zeros((9, 2))
# Doing the above least square estimation by taking different columns of fitting.dat file as data
for k in range(len(DataCol)):
    perr[k], *rest = lstsq(M, DataCol[k], rcond=None)
# Calculating Aerr and Berr for each lstsq estimation
Aerr = array([square(x[0]-p[0]) for x in perr])
Berr = array([square(x[1]-p[1]) for x in perr])
plot(sigma, Aerr, 'o--', label='$A_{err}$')
plot(sigma, Berr, 'o--', label='$B_{err}$')
xlabel("$\sigma_{noise}$")
title("Variation of error with noise")
ylabel("Error in Esimation of A and B")
legend()
grid()
plt.savefig('Figure3.png')
show()

# Part 11
#Plotting a new diagram
figure(4)
# Plotting Aerr and Berr vs. sigma in a log-log scale
loglog(sigma, Aerr, 'ro', label="$A_{err}$")
loglog(sigma, Berr, 'bo', label="$B_{err}$")
legend()
errorbar(sigma, Aerr, std(Aerr), fmt='ro')
errorbar(sigma, Berr, std(Berr), fmt='bo')
xlabel("Log of $\sigma_{noise}$")
title("Variation of error with noise")
ylabel("Log of error")
legend(loc='upper right')
grid()
plt.savefig('Figure4.png')
show()
