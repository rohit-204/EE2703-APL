                                       # Assignment 4
									   #Rohit Kumar
									   #EE20B110




# Importing the required modules.	
from scipy import integrate
from pylab import *


                                
def expo(x):                        #Declearation of neccessary functions
	return exp(x)

def coscos(x):
	return cos(cos(x))

def u_exp(x,k):
	return expo(x)*cos(k*x)

def u_coscos(x,k):
	return coscos(x)*cos(k*x)	

def v_exp(x,k):
	return expo(x)*sin(k*x)

def v_coscos(x,k):
	return coscos(x)*sin(k*x)	

                                    
x = linspace(-2*pi,4*pi,1200)       #  defining x for values from -2π to 4π.


y_exp = expo(x)                   # getting the corresponding function values for all x.
y_coscos = coscos(x)

# taking  Periodic result of expo() and cos(cos(x)). 
y_exp_pe = []
y_exp_pe[0:400] = y_exp[400:800]
y_exp_pe[400:800] = y_exp[400:800]
y_exp_pe[800:1200] = y_exp[400:800]

y_coscos_pe = []
y_coscos_pe[0:400] = y_coscos[400:800]
y_coscos_pe[400:800] = y_coscos[400:800]
y_coscos_pe[800:1200] = y_coscos[400:800]


# Initializing all the required variables.
c_exp = empty((51,1))
c_coscos = empty((51,1))
sum_exp = 0
sum_coscos = 0
p=0
n = arange(1,52)


for k in range(26):          # loop to calculate the first 51 Fourier coefficients of the functions.

# The function integrate.quad() is used to find the value of the Fourier coefficients.	
	a_exp = integrate.quad(u_exp,0,2*pi,args=(k))[0]/pi
	b_exp = integrate.quad(v_exp,0,2*pi,args=(k))[0]/pi
	a_coscos = integrate.quad(u_coscos,0,2*pi,args=(k))[0]/pi
	b_coscos = integrate.quad(v_coscos,0,2*pi,args=(k))[0]/pi

# The corresponding Fourier series and coefficients are calculated and stored.
	if k==0:
		sum_exp += a_exp/2
		sum_coscos += a_coscos/2
		c_exp[p][0]  = a_exp/2
		c_coscos[p][0] = a_coscos/2 
		p = p + 1

	else:
		sum_exp += a_exp*cos(k*x) + b_exp*sin(k*x)	
		sum_coscos += a_coscos*cos(k*x) + b_coscos*sin(k*x)	
		c_exp[p][0] = a_exp
		c_coscos[p][0] = a_coscos
		c_exp[p+1][0] = b_exp
		c_coscos[p+1][0] = b_coscos
		p = p + 2

# The below set of codes will find the values of the Fourier coefficients using the lstsq() function.

xl=linspace(0,2*pi,401)
xl=xl[:-1] 

B_exp = expo(xl)
B_coscos = coscos(xl) 

A = zeros((400,51))
A[:,0] = 1
for k in range(1,26):
	A[:,2*k-1] = cos(k*xl)
	A[:,2*k] = sin(k*xl)

cl_exp = lstsq(A,B_exp,rcond=None)[0]
cl_coscos = lstsq(A,B_coscos,rcond=None)[0]

# The difference and deviation between the actual and predicted values are calculated.

diff_exp = abs(cl_exp - c_exp)
diff_coscos = abs(cl_coscos - c_coscos)

dev_exp = diff_exp.max()
dev_coscos = diff_coscos.max()

print("The deviation between coefficients for exp() is ",dev_exp)
print("The deviation between coefficients for coscos() is ",dev_coscos)

#The function values are calculated using the predicted Fourier coefficients.

yl_exp = dot(A,cl_exp)
yl_coscos = dot(A,cl_coscos)

# All the plots that are asked are as shown below.




figure(1)     # plot for exp vs x
semilogy(x,y_exp,label='True')
title("Figure 1a")
xlabel(r'$x\rightarrow$',size=15)
ylabel(r'$e^x\rightarrow$',size=15)
grid(True)
legend()

figure(2)           #   exp vs x  (predicted)  semilog
semilogy(x,y_exp,label='True')
semilogy(x,y_exp_pe,label='Periodic Extension')
title("Figure 1p")
xlabel(r'$x\rightarrow$',size=15)
ylabel(r'$e^x\rightarrow$',size=15)
grid(True)
legend()

figure(3)            #exp vs  x  (periodic extension) semilog
semilogy(x,y_exp,label='True')
semilogy(xl,yl_exp,'og',label='Predicted')
semilogy(x,y_exp_pe,label='Periodic Extension')
title("Figure 1")
xlabel(r'$x\rightarrow$',size=15)
ylabel(r'$e^x\rightarrow$',size=15)
grid(True)
legend()


figure(4)    #cos(cosx)  vs  x
plot(x,y_coscos,label='True')
title("Figure 2a")
xlabel(r'$x\rightarrow$',size=15)
ylabel(r'$cos(cos(x))\rightarrow$',size=15)
grid(True)
legend()



figure(5)            #cos(cosx)  vs  x  (periodic extension)
plot(x,y_coscos,label='True')
plot(x,y_coscos_pe,label='Periodic Extension')
title("Figure 2")
xlabel(r'$x\rightarrow$',size=15)
ylabel(r'$cos(cos(x))\rightarrow$',size=15)
grid(True)
legend()

figure(6)           #cos(cosx)  vs  x  (predicted)
plot(x,y_coscos,label='True')
plot(xl,yl_coscos,'og',label='Predicted')
plot(x,y_coscos_pe,label='Periodic Extension')
title("Figure 2")
xlabel(r'$x\rightarrow$',size=15)
ylabel(r'$cos(cos(x))\rightarrow$',size=15)
grid(True)
legend()


figure(7)            #fourier coefficient  vs n  (semilog)
semilogy(n,abs(c_exp),'or',label='True')
title("Figure 3a")
xlabel(r'$n\rightarrow$',size=15)
ylabel(r'$coefficients\rightarrow$',size=15)
grid(True)
legend()


figure(8)             #fourier coefficient  vs n  (semilog) (predicted)
semilogy(n,abs(c_exp),'or',label='True')
semilogy(n,abs(cl_exp),'og',label='Predicted')
title("Figure 3")
xlabel(r'$n\rightarrow$',size=15)
ylabel(r'$coefficients\rightarrow$',size=15)
grid(True)
legend()


figure(9)            #fourier coefficient  vs n  (log)
loglog(n,abs(c_exp),'or',label='True')
title("Figure 4")
xlabel(r'$n\rightarrow$',size=15)
ylabel(r'$coefficients\rightarrow$',size=15)
grid(True)
legend()


figure(10)            #fourier coefficient  vs n  (log)  (predicted)
loglog(n,abs(c_exp),'or',label='True')
loglog(n,abs(cl_exp),'og',label='Predicted')
title("Figure 4")
xlabel(r'$n\rightarrow$',size=15)
ylabel(r'$coefficients\rightarrow$',size=15)
grid(True)
legend()

figure(11)      #fourier coefficient  vs n  (semilog)  
semilogy(n,abs(c_coscos),'or',label='True')
title("Figure 5a")
xlabel(r'$n\rightarrow$',size=15)
ylabel(r'$coefficients\rightarrow$',size=15)
grid(True)
legend()

figure(12)           #fourier coefficient  vs n  (semilog)  (predicted)
semilogy(n,abs(c_coscos),'or',label='True')
semilogy(n,abs(cl_coscos),'og',label='predicted')
title("Figure 5")
xlabel(r'$n\rightarrow$',size=15)
ylabel(r'$coefficients\rightarrow$',size=15)
grid(True)
legend()


figure(13)         #fourier coefficient  vs n  (log)  
loglog(n,abs(c_coscos),'or',label='True')
title("Figure 6a")
xlabel(r'$n\rightarrow$',size=15)
ylabel(r'$coefficients\rightarrow$',size=15)
grid(True)
legend()



figure(14)        #fourier coefficient  vs n  (log)  (predicted)
loglog(n,abs(c_coscos),'or',label='True')
loglog(n,abs(cl_coscos),'og',label='Predicted')
title("Figure 6")
xlabel(r'$n\rightarrow$',size=15)
ylabel(r'$coefficients\rightarrow$',size=15)
grid(True)
legend()

show()