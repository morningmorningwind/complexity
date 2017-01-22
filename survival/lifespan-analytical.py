# encoding: utf-8
import os
import csv
from pylab import *
from numpy import *
from loadData import loadData
from mymath import statistic, revcumsum
from random import sample as spl
from scipy.special import erf

def fit(t,u,T,d=0.5):
    return (u*erf((t*u)/(2.0*sqrt(d*t))) + ((exp(-((t*u**2.0)/(4.0*d))) - exp(-((T - t*u)**2.0/(4.0*d*t))))*\
       sqrt(d*t) + sqrt(pi)*t*u*erf((T - t*u)/(2.0*sqrt(d*t))))/(sqrt(pi)*t))/T/\
  (1.0 + 2.0*sqrt(d/(pi*T))*(-exp(-((T*(-1.0 + u)**2.0)/(4.0*d))) + exp(-((T*u**2.0)/(4.0*d)))) +\
   u*erf((T*u)/(2.0*sqrt(d*T))) + (-1.0 + u)*erf((T - T*u)/(2.0*sqrt(d*T))))
T=320
f1=figure(1,figsize=(6,4))
#colors={0:'red',1:'green',2:'blue'}
P=[0.46,0.48,0.5,0.52,0.54]
x=linspace(1,T,1000)
for i in range(len(P)):
    _=loglog(x,fit(x,(2*P[i]-1.0),T),label=r'$p=$'+str(P[i]))
xlim([1,340])
ylim([1e-4,1])
xlabel(r'Lifespan [day]')
ylabel(r'Fraction')
legend(loc='best')
f1.set_tight_layout(True)
savefig('figs/Lifespan-analytical.pdf', format='pdf')
close(1)
