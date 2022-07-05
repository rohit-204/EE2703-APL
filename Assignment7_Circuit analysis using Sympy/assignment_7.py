from numpy import *
from pylab import *
from sympy import  *
import scipy.signal as sp
import matplotlib.pyplot as plt
s=symbols('s')
def lowpassfilter(R1,R2,C1,C2,G,Vi):
    A=Matrix([[0,0,1,-1/G],[-1/(1+s*R2*C2),1,0,0],[0,-G,G,1],[-1/R1-1/R2-s*C1,1/R2,0,s*C1]])
    b=Matrix([0,0,0,Vi/R1])
    v=A.inv()*b
    return A,b,v

A,b,v= lowpassfilter(10000,10000,1e-9,1e-9,1.586,1)

H=v[3]

def sympytotrnfn(func):
    num, den = simplify(func).as_numer_denom()
    num_list=Poly(num).all_coeffs()
    num_list = array(num_list, dtype='double')
    den_list=Poly(den).all_coeffs()
    den_list = array(den_list, dtype='double')
    h_lowpass=sp.lti(num_list,den_list)
    return h_lowpass

h_lowpass=sympytotrnfn(H)

t=linspace(0,0.001,1000)
Vi = np.multiply((np.sin(2000*np.pi*t)+np.cos(2000000*np.pi*t)),np.heaviside(t,1))
c=heaviside(t,0)
t,y,svec=sp.lsim(h_lowpass,c,t)
plt.plot(t,c,label='V_input')
plt.plot(t, y,label='V_output')
xlabel("t"+"$\\rightarrow$")
ylabel("V"+"$\\rightarrow$")
title("step response of the circuit")
grid(True)
legend()
show() 

t,y,svec=sp.lsim(h_lowpass,Vi,t)
plt.plot(t,Vi,label='V_input')
plt.plot(t,y,label='V_output')
xlabel("t"+"$\\rightarrow$")
ylabel("V"+"$\\rightarrow$")
title("response of the circuit to vi(t) =(sin(2000πt)+cos(2*10^6πt))*u(t)")
plt.grid(True)
legend()
show()

def highpassfilter(R1,R2,C1,C2,G,Vi):
    A = Matrix([[0,0,1,-1/G],[-s*C2,(1/R2) +s*C2,0,0],[0,-G,G,1],[0-s*C1-s*C2-1/R1,s*C2,0,1/R1]])
    b = Matrix([0,0,0,Vi*s*C1])
    v=A.inv()*b
    return A,b,v

A_high,b_high,v_high=highpassfilter(10000,10000,1e-9,1e-9,1.586,1)
trnsfrfunc=v_high[3] 
print(trnsfrfunc)


h_highpass=sympytotrnfn(trnsfrfunc)
print(h_highpass)
ww=logspace(0,8,801)
ss=1j*ww
hf=lambdify(s,trnsfrfunc,'numpy')
v=hf(ss)
plt.loglogx(ww,abs(v),lw=2)
plt.grid(True)
title("Transfer function of highpass filter ")
xlabel("w"+"$\\rightarrow$")
ylabel("|H(s)|"+"$\\rightarrow$")
plt.show()


t=linspace(0,10,10000)
vi = np.multiply(np.multiply(np.exp(-0.5*t),np.sin(2*np.pi*t)),np.heaviside(t,0.5))
plt.plot(t,vi,label='V_input')
t,y,svec=sp.lsim(h_highpass,vi,t)
title("vo when vi is sinusoidal deacying")
plt.plot(t,y,label='V_output')
title("response of the circuit at low w ")
xlabel("t"+"$\\rightarrow$")
ylabel("V"+"$\\rightarrow$")
grid(True)
legend()
show()


t=linspace(0,0.001,10000)
vi = np.multiply(np.multiply(np.exp(-5000*t),np.sin(2*np.pi*1e4*t)),np.heaviside(t,0.5))
plt.plot(t,vi,label='V_input')
t,y,svec=sp.lsim(h_highpass,vi,t)
plt.plot(t,y,label='V_output')
title("response of the circuit at high w ")
xlabel("t"+"$\\rightarrow$")
ylabel("V"+"$\\rightarrow$")
plt.grid(True)
legend()
show()


t=linspace(0,0.001,10000)
vi=heaviside(t,0)
plt.plot(t,vi,label='V_input')
t,y,svec=sp.lsim(h_highpass,vi,t)
plt.plot(t,y,label='V_output')
xlabel("t"+"$\\rightarrow$")
ylabel("V"+"$\\rightarrow$")
title("step response of the circuit")
plt.grid(True)
legend()
show()

