"""
Assignment 6B
Date    : 11th May 2021
Course  : Applied Programming Lab(EE2703)
Faculty : Prof. Harishankar Ramachandhran

Submission by : Santosh G (EE19B055)

To compile and execute: python3 EE2703_ASSIGN6B_EE19B055.py

"""
from pylab import *
import scipy.signal as sp

# Question 1
p11 = poly1d([1,0.5])					#Defining Numerator
p12 = polymul([1,1,2.5],[1,0,2.25])			#Defining Denominator 
X1 = sp.lti(p11,p12)					#Defining the transfer function 
t1,x1 = sp.impulse(X1,None,linspace(0,50,500))	#Solving for the impulse reponse

# Question 1 Plots
figure(1)
plot(t1,x1)
title("Soln plot x(t) for Q1")
xlabel(r'$t\rightarrow$')
ylabel(r'$x(t)\rightarrow$')
grid(True)
plt.savefig("Figure 1.png")

#Question 2
p21 = poly1d([1,0.05])
p22 = polymul([1,0.1,2.2525],[1,0,2.25])
X2 = sp.lti(p21,p22)
t2,x2 = sp.impulse(X2,None,linspace(0,50,500))

#Question 2 Plots
figure(2)
plot(t2,x2)
title("Soln plot x(t) for Q2")
xlabel(r'$t\rightarrow$')
ylabel(r'$x(t)\rightarrow$')
grid(True)
plt.savefig("Figure 2.png")

#Question 3
H = sp.lti([1],[1,0,2.25])
for w in arange(1.4,1.6,0.05):
	t = linspace(0,50,500)
	f = cos(w*t)*exp(-0.05*t)
	t,x,svec = sp.lsim(H,f,t)

#Plot of x(t) with varying freqs vs time for Q3
	figure(3)
	plot(t,x,label='w = ' + str(w))
	title("x(t) for various frequencies")
	xlabel(r'$t\rightarrow$')
	ylabel(r'$x(t)\rightarrow$')
	legend(loc = 'upper left')
	grid(True)
	plt.savefig("Figure 3.png")
	
#Question 4
t4 = linspace(0,20,500)
X4 = sp.lti([1,0,2],[1,0,3,0])
Y4 = sp.lti([2],[1,0,3,0])	
t4,x4 = sp.impulse(X4,None,t4)
t4,y4 = sp.impulse(Y4,None,t4)

# The plot of x(t) and y(t) vs t for Q4 
figure(4)
plot(t4,x4,label='x(t)')
plot(t4,y4,label='y(t)')
title("y(t) & x(t) vs time")
xlabel(r'$t\rightarrow$')
ylabel(r'$functions\rightarrow$')
legend(loc = 'upper right')
grid(True)
plt.savefig("Figure 4.png")

#Question 5
temp = poly1d([1e-12,1e-4,1])
H5 = sp.lti([1],temp)
w,S,phi = H5.bode()

# The magnitude and phase bode plots for Q5 
figure(5)
semilogx(w,S)
title("Magnitude Bode plot")
xlabel(r'$\omega\rightarrow$')
ylabel(r'$20\log|H(j\omega)|\rightarrow$')
grid(True)
plt.savefig("Figure 5a.png")
 
figure(6)
semilogx(w,phi)
title("Phase Bode plot")
xlabel(r'$\omega\rightarrow$')
ylabel(r'$\angle H(j\omega)\rightarrow$')
grid(True)
plt.savefig("Figure 5b.png")

#Question 6
t6 = arange(0,25e-3,1e-7)
vi = cos(1e3*t6) - cos(1e6*t6)
t6,vo,svec = sp.lsim(H5,vi,t6)

# The plot of Vo(t) vs t for large time interval for Q6
figure(7)
plot(t6,vo)
title("The Output Voltage for large time interval")
xlabel(r'$t\rightarrow$')
ylabel(r'$V_o(t)\rightarrow$')
grid(True)
plt.savefig("Figure 6a.png")

# The plot of Vo(t) vs t for small time interval for Q6
figure(8)
plot(t6[0:300],vo[0:300])
title("The Output Voltage for small time interval")
xlabel(r'$t\rightarrow$')
ylabel(r'$V_o(t)\rightarrow$')
grid(True)
plt.savefig("Figure 6b.png")

print("Computations have been completed successfully, Please find the diagrams in the same folder")
