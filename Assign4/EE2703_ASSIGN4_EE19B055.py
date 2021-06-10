"""
Assignment 4
Date    : 12th March 2021
Course  : Applied Programming Lab(EE2703)
Faculty : Prof. Harishankar Ramachandhran

Submission by : Santosh G (EE19B055)

To complie and execute: python3 EE2703_ASSIGN4_EE19B055.py

"""
import numpy as np
from scipy.integrate import quad
from matplotlib import pyplot as plt
from pylab import *
import scipy.special as sp

def ccFun(x):
    return np.cos(np.cos(x))
def eFun(x):
    return np.exp(x)

def pi_tick(value, tick_num):
    # find number of multiples of pi/2
    N = int(round(2 * value / PI))
    if N == 0:
        return "0"
    elif N == 1:
        return r"$\pi/2$"
    elif N == -1:
        return r"$-\pi/2$"
    elif N == 2:
        return r"$\pi$"
    elif N == -2:
        return r"$-\pi$"
    elif N % 2 != 0:
        return r"${0}\pi/2$".format(N)
    else:
        return r"${0}\pi$".format(N//2)

PI = np.pi
x = np.linspace(-2*PI, 4*PI, 401)
x = x[:-1]

plt.figure('Figure 1')
ax2 = plt.axes()
ax2.xaxis.set_major_formatter(plt.FuncFormatter(pi_tick))
plt.semilogy(x, eFun(x), 'k', label='True Function', color='red')
plt.semilogy(x, eFun(x%(2*PI)), '--', label='Fourier Series expansion')
plt.legend(loc='upper left')
plt.title('$e^x$')
plt.grid()
plt.savefig('Figure 1.png')

plt.figure('Figure 2')
ax1 = plt.axes()
ax1.xaxis.set_major_formatter(plt.FuncFormatter(pi_tick))
plt.plot(x, ccFun(x), 'k', label='True Function', color = 'red')
plt.plot(x, ccFun(x%(2*PI)), '--', label='Fourier Series expansion')
plt.axis([-6, 10, 0.5, 1.05])
plt.legend(loc='upper right')
plt.title('$cos(cos(x))$')
plt.grid()
plt.savefig('Figure 2.png')

def cosCoeff(x, k, f):
    return f(x)*np.cos(k*x)
def sinCoeff(x, k, f):
    return f(x)*np.sin(k*x)

def calc51FCoeffs (f):
    aCoeff = np.zeros(26)
    bCoeff = np.zeros(26)
    aCoeff[0] = quad(cosCoeff, 0, 2*PI, args=(0, f))[0]/(2*PI)
    for i in range(1, 26):
        aCoeff[i] = quad(cosCoeff, 0, 2*PI, args=(i, f))[0]/(PI)
        bCoeff[i] = quad(sinCoeff, 0, 2*PI, args=(i, f))[0]/(PI)
    coeffs = np.zeros(51)
    coeffs[0] = aCoeff[0]
    coeffs[1::2] = aCoeff[1:]
    coeffs[2::2] = bCoeff[1:]
    return coeffs

coeffCC = calc51FCoeffs(ccFun)
coeffE = calc51FCoeffs(eFun)

xTicksCoeffsSemilog = ['$a_0$']
for i in range(1, 26):
    xTicksCoeffsSemilog.append('${'+str(i)+'}$')

plt.figure('Figure 3')
plt.xticks(np.arange(26), xTicksCoeffsSemilog, rotation=60)
plt.tick_params(axis='x', labelsize=7)
plt.xlabel('n')
plt.semilogy(abs(coeffE[1::2]), 'bo', label='$a_n$')
plt.semilogy(abs(coeffE[2::2]), 'ro', label='$b_n$')
plt.legend()
plt.title('$e^x$ Semilogy plot')
plt.grid()
plt.savefig('Figure 3.png')

plt.figure('Figure 4')
plt.loglog(abs(coeffE[1::2]), 'bo', label='$a_n$')
plt.loglog(abs(coeffE[2::2]), 'ro', label='$b_n$')
plt.legend()
plt.title('$e^x$ LogLog plot')
plt.grid()
plt.savefig('Figure 4.png')

plt.figure('Figure 5')
plt.xticks(np.arange(26), xTicksCoeffsSemilog, rotation=60)
plt.tick_params(axis='x', labelsize=7)
plt.semilogy(abs(coeffCC[1::2]), 'bo', label='$a_n$')
plt.semilogy(abs(coeffCC[2::2]), 'ro', label='$b_n$')
plt.xlabel('n')
plt.legend()
plt.title('$cos(cos(x))$ Semilogy plot')
plt.grid()
plt.savefig('Figure 5.png')

plt.figure('Figure 6')
plt.loglog(abs(coeffCC[1::2]), 'bo', label='$a_n$')
plt.loglog(abs(coeffCC[2::2]), 'ro', label='$b_n$')
plt.legend()
plt.title('$cos(cos(x))$ LogLog plot')
plt.grid()
plt.savefig('Figure 6.png')


def LSTSQCoeff(f):
    x = np.linspace(0, 2*PI, 401)
    x = x[:-1]
    b = f(x)
    M = np.zeros((400, 51))
    M[:,0] = 1
    for k in range(1,26):
        M[:,(2*k)-1]=np.cos(k*x)
        M[:,2*k]=np.sin(k*x)
    return np.linalg.lstsq(M, b, rcond=None)[0]

lstsqCC = LSTSQCoeff(ccFun)
lstsqE  = LSTSQCoeff(eFun)

plt.figure('Figure 3.1')
plt.semilogy(abs(coeffE[1::2]), 'ro', label='$a_n$ by Integration')
plt.semilogy(abs(coeffE[2::2]), 'bo', label='$b_n$ by Integration')
plt.semilogy(abs(lstsqE[1::2]), 'go', label='$a_n$ by lstsq')
plt.semilogy(abs(lstsqE[2::2]), 'yo', label='$b_n$ by lstsq')
plt.title('Comparing $e^x$ FS coefficients - semilogy plot')
plt.legend()
plt.grid()
plt.savefig('Figure 3.1.png')

plt.figure('Figure 4.1')
plt.loglog(abs(coeffE[1::2]), 'ro', label='$a_n$ by Integration')
plt.loglog(abs(coeffE[2::2]), 'bo', label='$b_n$ by Integration')
plt.loglog(abs(lstsqE[1::2]), 'go', label='$a_n$ by lstsq')
plt.loglog(abs(lstsqE[2::2]), 'yo', label='$b_n$ by lstsq')
plt.title('Comparing $e^x$ FS coefficients - loglog plot')
plt.legend()
plt.grid()
plt.savefig('Figure 4.1.png')

plt.figure('Figure 5.1')
plt.semilogy(abs(coeffCC[1::2]), 'ro', label='$a_n$ by Integration')
plt.semilogy(abs(coeffCC[2::2]), 'bo', label='$b_n$ by Integration')
plt.semilogy(abs(lstsqCC[1::2]), 'go', label='$a_n$ by lstsq')
plt.semilogy(abs(lstsqCC[2::2]), 'yo', label='$b_n$ by lstsq')
plt.title('Comparing $cos(cos(x))$ FS coefficients - semilogy plot')
plt.legend()
plt.grid()
plt.savefig('Figure 5.1.png')

plt.figure('Figure 6.1')
plt.loglog(abs(coeffCC[1::2]), 'ro', label='$a_n$ by Integration')
plt.loglog(abs(coeffCC[2::2]), 'bo', label='$b_n$ by Integration')
plt.loglog(abs(lstsqCC[1::2]), 'go', label='$a_n$ by lstsq')
plt.loglog(abs(lstsqCC[2::2]), 'yo', label='$b_n$ by lstsq')
plt.title('Comparing $cos(cos(x))$ FS coefficients - loglog plot')
plt.legend()
plt.grid()
plt.savefig('Figure 6.1.png')

absErrCC = [abs(coeffCC[i]-lstsqCC[i]) for i in range(len(coeffCC))]
absErrE = [abs(coeffE[i]-lstsqE[i]) for i in range(len(coeffE))]

print('Max. deviation for cos(cos(x)): '+str(max(absErrCC)))
print('Max. deviation for exp(x): '+str(max(absErrE)))

xNew = np.linspace(0, 2*PI, 401)
xNew = xNew[:-1]

matrixA = np.zeros((400,51))
matrixA[:,0] = 1
for k in range(1,26):
    matrixA[:,(2*k)-1]=np.cos(k*xNew)
    matrixA[:,2*k]=np.sin(k*xNew)

plt.figure('Figure 7')
ax3 = plt.axes()
ax3.xaxis.set_major_formatter(plt.FuncFormatter(pi_tick))
plt.semilogy(xNew, matrixA@coeffCC, 'go', label='Integration')
plt.semilogy(xNew, ccFun(xNew), 'k', label='True Function')
plt.semilogy(xNew, matrixA@lstsqCC, 'r', label='lstsq')
plt.title('Reconstruction of $cos(cos(x))$')
plt.legend()
plt.grid()
plt.savefig('Figure 7.png')

plt.figure('Figure 8')
ax4 = plt.axes()
ax4.xaxis.set_major_formatter(plt.FuncFormatter(pi_tick))
plt.semilogy(xNew, matrixA@coeffE, 'go', label='Integration')
plt.semilogy(xNew, eFun(xNew), 'k', label='True Function')
plt.semilogy(xNew, matrixA@lstsqE, 'r', label='lstsq')
plt.title('Reconstruction of $e^x$')
plt.legend()
plt.grid()
plt.savefig('Figure 8.png')
