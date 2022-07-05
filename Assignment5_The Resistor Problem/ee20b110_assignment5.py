#										Assignment  5
#                                       Rohit Kumar
#                                       Ee20b110			 
#																			      
from pylab import *           # Importing the required modules.
import sys
import mpl_toolkits.mplot3d.axes3d as p3

# Initializing the required parameters with their default values.
Nx = 25 
Ny = 25
radius = 8
Niter = 1500 

# Required parameters can also be given through the commmand line.
if(len(sys.argv)>1):
	Nx = int(sys.argv[1])
	Ny = int(sys.argv[2])
	Niter = int(sys.argv[3])

# Creating the respective matrices and initializing them also.
phi = zeros((Ny,Nx))
x = linspace(-0.5,0.5,Nx)
y = linspace(-0.5,0.5,Ny)
n = arange(Niter)
X,Y = meshgrid(x,-y)

# The coordinates can be got for the points inside the given radius.
A = (X*X) + (Y*Y)
ii = where(A <= (0.35*0.35))

# Setting the value of Phi as 1.0 at those coordinates.
phi[ii] = 1.0

# The below piece of code is to perform the iteration and to calculate the error in the potential.
errors = empty((Niter,1))
for k in range(Niter):
	oldphi = phi.copy()
	phi[1:-1,1:-1] = 0.25*(phi[1:-1,0:-2] + phi[1:-1,2:] + phi[0:-2,1:-1] + phi[2:,1:-1])

# These lines will set the proper boundary conditions.
	phi[1:-1,0] = phi[1:-1,1]
	phi[1:-1,-1] = phi[1:-1,-2]
	phi[0,1:-1] = phi[1,1:-1]
	phi[ii] = 1.0
	errors[k]=(abs(phi-oldphi)).max()

# The exponent part of the error values can be got using the below piece of code.
c_approx_500 = lstsq(c_[ones(Niter-500),arange(500,Niter)],log(errors[500:]),rcond=None)
a_500,b_500 = exp(c_approx_500[0][0]),c_approx_500[0][1]
print("The values of A and B for the iterations after 500 are: ",a_500,b_500)

c_approx = lstsq(c_[ones(Niter),arange(Niter)],log(errors),rcond=None)
a, b = exp(c_approx[0][0]), c_approx[0][1]
print("The values of A and B are: ",a,b)

# The current density vectors can be calulated as shown.
Jx = zeros((Ny, Nx))
Jy = zeros((Ny, Nx))
Jx[1:-1, 1:-1] = 0.5*(phi[1:-1, 0:-2] - phi[1:-1, 2:])
Jy[1:-1, 1:-1] = 0.5*(phi[2:, 1:-1] - phi[0:-2, 1:-1])

# plotting of the current vector plot along with the potential.
figure(0)
quiver(X,Y,Jx,Jy)
plot(ii[0]/Nx-0.48,ii[1]/Ny-0.48,'ro')
title("The vector plot of the current flow")
xlabel(r'$X\rightarrow$')
ylabel(r'$Y\rightarrow$')

# Plotting of the initial potential contour.
figure(1)
plot(ii[0]/Nx-0.48,ii[1]/Ny-0.48,'ro',label="V = 1")
title("Initial Potential Contour")
xlim(-0.5,0.5)
ylim(-0.5,0.5)
xlabel(r'$X\rightarrow$')
ylabel(r'$Y\rightarrow$')
grid(True)
legend()

# Plotting of error vs iteration in semilog.
figure(2)
semilogy(n,errors)
title("Error versus iteration")
xlabel(r'$Iteration\rightarrow$',size=15)
ylabel(r'$Error\rightarrow$',size=15)
grid(True)

# Plotting of error vs iteration in loglog.
figure(3)
loglog(n,errors)
title("Error versus iteration in a loglog plot")
xlabel(r'$Iteration\rightarrow$',size=15)
ylabel(r'$Error\rightarrow$',size=15)
grid(True)

# Plotting of error vs iteration above 500 in semilog .
figure(4)
semilogy(n[500:],errors[500:])
title("Error versus iteration above 500")
xlabel(r'$Iteration\rightarrow$',size=15)
ylabel(r'$Error\rightarrow$',size=15)
grid(True)

# Plotting of actual and expected error (above 500 iterations) in semilog.
figure(5)
semilogy(n[500:],errors[500:],label="Actual")
semilogy(n[500:],a_500*exp(b_500*n[500:]),label="Expected")
title("Expected versus actual error (>500 iterations)")
xlabel(r'$Iteration\rightarrow$',size=15)
ylabel(r'$Error\rightarrow$',size=15)
grid(True)
legend()

# Plotting of the actual and expected error in semilog.
figure(6)
semilogy(n,errors,label="Actual")
semilogy(n,a*exp(b*n),label="Expected")
title("Expected versus actual error ")
xlabel(r'$Iteration\rightarrow$',size=15)
ylabel(r'$Error\rightarrow$',size=15)
grid(True)
legend()

# Plotting of the contour of phi (potential).
figure(7)
contourf(X,Y,phi)
plot(ii[0]/Nx-0.48,ii[1]/Ny-0.48,'ro',label="V = 1")
title("Contour plot of potential")
xlabel(r'$X\rightarrow$')
ylabel(r'$Y\rightarrow$')
colorbar()
grid(True)
legend()

# Plotting the surface plots of phi (potential).
fig1=figure(8)
ax=p3.Axes3D(fig1) 
title("The 3-D surface plot of the potential")
xlabel(r'$X\rightarrow$')
ylabel(r'$Y\rightarrow$')
surf = ax.plot_surface(X, Y, phi, rstride=1, cstride=1, cmap=cm.jet)
fig1.colorbar(surf)

show()
