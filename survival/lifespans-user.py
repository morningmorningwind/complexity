import os
import csv
from pylab import *
from numpy import *
import pickle
from itertools import cycle
from mymath import statistic,revcumsum,sortxy,rmean,readCSV
from random import sample as spl
import powerlaw as plw
from scipy.stats import weibull_min,linregress
from truncatedweilbull import TruWeil

L=readCSV('userLifespan.txt','sav/')
for i in range(len(L)):
    L[i]=float(L[i][1])
f1=figure(1,figsize=(6,4))
f1.clf()
L=array(L,dtype=float)
fit1=plw.Fit(L,xmin=1,xmax=319,discrete=True)
a=TruWeil(L)
afit=a.fit()
pdf=afit['pdf']
beta=afit['beta']
eta=afit['eta']
ax1=fit1.plot_pdf(original_data=True,color='k',label='empirical data')
#fit1.power_law.plot_pdf(ax=ax1,color='r',linestyle='--',linewidth=2,label=r'fitting: $\alpha='+('%.3f' % fit1.power_law.alpha)+'$')
x=linspace(1.5,330.0,1000)
ax1.loglog(x,pdf(x),color='r',linestyle='--',linewidth=2,label=r'fitting:$\beta='+str(round(beta,3))+', '+'\eta='+str(round(eta,3))+'$')
#fit2=plw.Fit(L1,xmin=1,xmax=100,discrete=True)
#fit2.plot_pdf(ax=ax1,original_data=True,color='lime',linestyle='-.',linewidth=2,label='null model')
xlabel(r'Life Span [day]')
ylabel(r'PDF')
ylim([1e-4,1])
legend(loc='best')
f1.set_tight_layout(True)
savefig('figs/lifespan-PDF-truncatedWeilbull-users.pdf', format='pdf') 
