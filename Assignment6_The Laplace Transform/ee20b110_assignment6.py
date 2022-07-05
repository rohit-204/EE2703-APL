#						    ASSIGNMENT 6: THE LAPLACE TRANSFORM
#						   Rohit Kumar Ee20b110
# Importing the necessary modules.
from pylab import *
import scipy.signal as sp

#   code to find time response  x¨+2.25x = f(t)
p11 = poly1d([1,0.5])
p21 = polymul([1,1,2.5],[1,0,2.25])
X1 = sp.lti(p11,p21)
t1,x1 = sp.impulse(X1,None,linspace(0,50,1500))

figure(0)
plot(t1,x1)
title("The solution x(t) for Q.1")
xlabel(r'$t\rightarrow$')
ylabel(r'$x(t)\rightarrow$')
grid(True)



# above response for smaller response
p12 = poly1d([1,0.05])
p22 = polymul([1,0.1,2.2525],[1,0,2.25])
X2 = sp.lti(p12,p22)
t2,x2 = sp.impulse(X2,None,linspace(0,50,1500))

figure(1)
plot(t2,x2)
title("The solution x(t) for Q.2")
xlabel(r'$t\rightarrow$')
ylabel(r'$x(t)\rightarrow$')
grid(True)




# code to obtain the system transfer function X(s)/F(s)
H = sp.lti([1],[1,0,2.25])
for w in arange(1.4,1.6,0.05):
	t = linspace(0,50,1500)
	f = cos(w*t)*exp(-0.05*t)
	t,x,svec = sp.lsim(H,f,t)

	figure(2)
	plot(t,x,label='w = ' + str(w))
	title("x(t) for different frequencies")
	xlabel(r'$t\rightarrow$')
	ylabel(r'$x(t)\rightarrow$')
	legend(loc = 'upper left')
	grid(True)



#  response for
#      x¨+ (x−y) = 0
#      y¨+2(y−x) = 0
t4 = linspace(0,20,1500)
X4 = sp.lti([1,0,2],[1,0,3,0])
Y4 = sp.lti([2],[1,0,3,0])	
t4,x4 = sp.impulse(X4,None,t4)
t4,y4 = sp.impulse(Y4,None,t4)

figure(3)
plot(t4,x4,label='x(t)')
plot(t4,y4,label='y(t)')
title("x(t) and y(t)")
xlabel(r'$t\rightarrow$')
ylabel(r'$functions\rightarrow$')
legend(loc = 'upper right')
grid(True)




# solving two port network
l=1e-6
c=1e-6
r=100.0
H5 = sp.lti([1],[l*c,r*c,1])
w,S,phi = H5.bode()

figure(4)
semilogx(w,S)
title("Magnitude Bode plot")
xlabel(r'$\omega\rightarrow$')
ylabel(r'$\|H(j\omega)|\rightarrow$')
grid(True)

figure(5)
semilogx(w,phi)
title("Phase Bode plot")
xlabel(r'$\omega\rightarrow$')
ylabel(r'$\angle H(j\omega)\rightarrow$')
grid(True)



# output voltage
t6 = arange(0,25e-3,1e-7)
vi = cos(1e3*t6) - cos(1e6*t6)
t6,v_out,svec = sp.lsim(H5,vi,t6)

figure(6)
plot(t6,v_out)
title("The Output Voltage for large time interval")
xlabel(r'$t\rightarrow$')
ylabel(r'$V_o(t)\rightarrow$')
grid(True)

figure(7)
plot(t6[0:300],v_out[0:300])
title("The Output Voltage for small time interval")
xlabel(r'$t\rightarrow$')
ylabel(r'$V_o(t)\rightarrow$')
grid(True)

show()