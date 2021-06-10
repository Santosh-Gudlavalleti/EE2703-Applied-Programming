"""
Assignment 5
Date    : 6th May 2021
Course  : Applied Programming Lab(EE2703)
Faculty : Prof. Harishankar Ramachandhran

Submission by : Santosh G (EE19B055)

To complie and execute: python3 EE2703_ASSIGN5_EE19B055.py

"""
import numpy as np
import scipy.linalg
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import argparse
import sys

#Taking Inputs 
parser = argparse.ArgumentParser()
parser.add_argument("--Nx", help='size along x', type=int, default=50, metavar='nx')
parser.add_argument("--Ny", help='size along y', type=int, default=50, metavar='ny')
parser.add_argument("--radius", help='radius of central lead', type=float, default=0.35, metavar='r')
parser.add_argument("--Niter", help='number of iterations to perform', type=int, default=4000, metavar='ni')
argv=parser.parse_argv()
[Nx, Ny, radius, Niter] = [argv.Nx, argv.Ny, argv.radius, argv.Niter]
print(Nx, Ny, radius)

phi = np.zeros((Nx, Ny), dtype=float)
x = np.linspace(-radius*1.25, radius*1.25, Nx)
y = np.linspace(-radius*1.25, radius*1.25, Ny)
X, Y = np.meshgrid(x, -y)
ax1 = plt.axes()
v1Nodes = np.where(np.square(X)+np.square(Y) <= radius**2)
phi[v1Nodes] = 1.0

plt.figure('Figure 1')                     #Plotting Contour Plot
contPlot = plt.contourf(X, Y, phi, cmap=cm.jet)
ax1.set_aspect('equal')
plt.colorbar(ax=ax1, orientation='vertical')
plt.title('Contour Plot of Potential $\phi$')
plt.savefig('Fig1.png')

itrn = []           #
error = []
for n in range(Niter):
    # Copy old phi
    oldphi = phi.copy()

    # Updating the Potential
    phi[1:-1, 1:-1] = 0.25*(phi[1:-1, 0:-2]+phi[1:-1, 2:]+phi[0:-2, 1:-1]+phi[2:, 1:-1])

    # Boundary Conditions
    phi[1:-1, 0] = phi[1:-1, 1]  # Left edge
    phi[1:-1, -1] = phi[1:-1, -2]  # right edge
    phi[0, :] = phi[1, :]  # Top edge
    #No boundary conditions for the bottom edge

    # Assigning 1V to electrode region
    phi[v1Nodes] = 1.0

    error.append(np.abs(phi-oldphi).max())
    itrn.append(n)

#Analyzing Error

plt.figure('Figure 2')
plt.semilogy(itrn, error)
ax1.set_aspect('equal')
plt.title('Semilog Plot of error')
plt.xlabel('Iteration')
plt.ylabel('Error')
plt.savefig('Fig2.png')

plt.figure('Figure 3')
plt.loglog(itrn, error)
plt.title('Loglog Plot of error')
plt.xlabel('Iteration')
plt.ylabel('Error')
plt.savefig('Fig3.png')

def findFit(errors, itrns):
    nRows = len(errors)
    coeffMat = np.zeros((nRows,2), dtype=float)
    constMat = np.zeros((nRows,1), dtype=float)
    coeffMat[:,0] = 1
    coeffMat[:,1] = itrns
    constMat = np.log(errors)
    fit = scipy.linalg.lstsq(coeffMat, constMat)[0]
    est = coeffMat@fit
    return fit, est

fitAll, estAll = findFit(error, itrn)
fitAfter500, estAfter500 = findFit(error[501:], itrn[501:])

#Comparing the Errors
plt.figure('Figure 4')
plt.semilogy(itrn[::200], np.exp(estAll[::200]), 'r.', mfc='none', label='fit all')
plt.semilogy(itrn[501::200], np.exp(estAfter500[::200]), 'y.', mfc='none', label='fit after 500')
plt.semilogy(itrn, error, 'g', label='actual error')
print('Fit 1 Results are\nA = {0} and  B = {1} \nFit2 Results are\nA = {2} and B = {3}\n'.format(np.exp(fitAll[0]), fitAll[1], np.exp(fitAfter500[0]), fitAfter500[1]))
plt.title('Comparison of actual errors and fits')
plt.xlabel('Iteration')
plt.ylabel('Error / fit')
plt.legend()
plt.savefig('Fig4.png')


def cumError(N, A, B):
    return -(A/B)*np.exp(B*(N+0.5))

def StopCond(errors, Niter, error_tol):
    cumErr = []
    for n in range(1, Niter):
        cumErr.append(cumError(n, np.exp(fitAll[0]), fitAll[1]))
        if(cumErr[n-1] <= error_tol):
            print("The change in the error during the last iteration is", (np.abs(cumErr[-1]-cumErr[-2])))
            return cumErr[n-1], n
    print("The change in the error during the last iteration is ", (np.abs(cumErr[-1]-cumErr[-2])))
    return cumErr[-1], Niter

errorTol = 10e-8
cumErr, nStop = StopCond(error, Niter, errorTol)
print("Stopping Conditions are N: %g and Error: %g" % (nStop, cumErr))

Fig5 = plt.figure('Figure 5')               # Plotting Surface plot
ax = p3.Axes3D(Fig5)
plt.title('The 3-D surface plot of $\phi$')
surfacePlot = ax.plot_surface(X, Y, phi, rstride=1, cstride=1, cmap=cm.jet)
cax = Fig5.add_axes([1, 0, 0.1, 1])
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.set_zlabel('$z$')
Fig5.colorbar(surfacePlot, cax=cax, orientation='vertical')
plt.savefig('Fig5.png')

plt.figure('Figure 6')                        # Plotting updated contour plot 
plt.contourf(X, Y, phi, cmap=cm.jet)
#ax = plt.axes()
ax1.set_aspect('equal')
plt.colorbar(ax=ax1, orientation='vertical')
plt.title('Updated Contour Plot of $\phi$')
plt.xlabel('x')
plt.ylabel('y')
plt.savefig('Fig6.png')

Jx = np.zeros((Ny,Nx))
Jy = np.zeros((Ny,Nx))

Jx[1:-1, 1:-1] = (phi[1:-1, 0:-2] - phi[1:-1, 2:])
Jy[1:-1, 1:-1] = (phi[2:, 1:-1] - phi[0:-2, 1:-1])

plt.figure('Figure 7')                     #Plotting Vector Current plot
plt.scatter(x[v1Nodes[0]], y[v1Nodes[1]], color='r', s=12, label='$V = 1V$ region')
plt.quiver(X, Y, Jx, Jy)
ax1.set_title('Vector Plot of current')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.savefig('Fig7.png')

