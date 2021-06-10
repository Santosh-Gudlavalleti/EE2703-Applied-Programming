"""
Assignment 6a
Date    : 10th May 2021
Course  : Applied Programming Lab(EE2703)
Faculty : Prof. Harishankar Ramachandhran

Submission by : Santosh G (EE19B055)

To compile and execute: python3 EE2703_ASSIGN6A_EE19B055.py

"""
import numpy as np
import matplotlib.pyplot as plt			
from tabulate import tabulate
from sys import argv


#Defining inputs and taking inputs 
if len(argv)==7:
	n=int(argv[1])
	M=int(argv[2])						
	nk=int(argv[3])
	u0=int(argv[4])
	p=float(argv[5])
	Msig=float(argv[6])
	
else:
	n=100	#No. of parts the tubelight is idvided into
	M=5	#Mean of Number of electrons injected per turn
	nk=500	#Number of turns to simulate
	u0=7	#Threshold velocity
	p=0.5	#Probability that ionization will occur
	Msig=2	#Standard deviation
	print("Note:")
	if len(argv) != 1:
		print("Improper number of inputs\n")			
	print("Default values are being used.To give custom inputs, type the 6 input values in the commandline in the follwing order\nn, M, nk, uo, p, Msig.\n")

#Initialising the position, velocity, displacement vectors.
#They are zero matrices which shall be updated.
xx=np.zeros(n*M)
u=np.zeros(n*M)					
dx=np.zeros(n*M)

#Initializing the light intensity, electron postion, electron velocity.
#They are empty lists which shall be updated using .extend.
I=[]
X=[]	
V=[]

#We find all those electrons whose position is greater than zero.
ii=np.where(xx>0)		 

for k in range(nk): 	
#<<The Block>>
	#Displacement increases due to electric field.
	dx[ii] = u[ii] + 0.5	

	#Advance the electron position and velocity for the turn.
	xx[ii] += dx[ii]	
	u[ii]  += 1
	
	#Determine the particles which have already hit the anode.
	jj = np.where(xx >= n)
	
	#Update their position and velocity to zero.	
	xx[jj] = 0			
	u[jj]  = 0
	
	#To find ionised electrons
	kk = np.where(u >= u0)[0]
	ll = np.where(np.random.rand(len(kk))<=p)
	kl = kk[ll]
	
	#Inelastic collision. Updating their velocities to zero.
	u[kl] = 0	
	
	#Generating a random number to find the point of collision.
	xx[kl] -= dx[kl]*np.random.rand(len(kl))	
	
	#Updating the I list with photons resulted an emission.
	I.extend(xx[kl].tolist())	
	
	#Adding new electrons.
	m  = int(np.random.randn()*Msig+M)	
	
	#Find the elctrons whose positions are zero.
	mm = np.where(xx == 0)	
	
	#Minimum of(no. of electrons to be added, no. of slots available.)
	minimum = min(len(mm[0]),m)	
	
	#Set their position to 1 and velocity to zero.
	xx[mm[0][:minimum]] = 1 	
	u[mm[0][:minimum]]  = 0 
	
	ii = np.where(xx > 0)
	
	#Add their positions to the X and V vectors.
	X.extend(xx[ii].tolist())	
	V.extend(u[ii].tolist())		
			
plt.figure("Figure 1.png")
plt.hist(X,bins=n,cumulative=False,edgecolor='black')	#Plot a histogram specifying the electron density
plt.title("Electron density")					#Set the title
plt.xlabel("$x$")						#set the x label
plt.ylabel("Number of electrons")				#Set the y label
plt.savefig("Figure 1.png")

plt.figure("Figure 2.png")
count,bins,trash = plt.hist(I,bins=n,edgecolor='black')	#Plot a histogram of the emission intensity of light
plt.title("Emission Intensity(I)")
plt.xlabel("$x$")
plt.ylabel("I")
plt.savefig("Figure 2.png")

plt.figure("Figure 3.png")
plt.scatter(X,V,marker='x')			#Plot the elctron phase space.
plt.title("Electron Phase Space")
plt.xlabel("Position")
plt.ylabel("Velocity")
plt.savefig("Figure 3.png")

plt.show()

xpos=0.5*(bins[0:-1]+bins[1:])		#Converting into midpoint values

file1 = open("data.txt","w")
file1.write("Intensity data:\n")
print("Intensity data:\n")
file1.close()
file1 = open("data.txt","a")
file1.write("xpos\tcount\n")
print("xpos\tcount\n") 
for k in range(len(count)):
	print(str(float("{0:.2f}". format(xpos[k])))+'\t'+str(int(count[k])))		#Print the table-like data showing population counts and the bin position
	L = [str(float("{0:.2f}". format(xpos[k])))+'\t'+str(int(count[k]))+'\n'] 
	file1.writelines(L)
file1.close()

print('The above data is also stored in "data.txt" and the images are also saved in the same folder.')
