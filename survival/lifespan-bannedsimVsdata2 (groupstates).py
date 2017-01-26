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

#data---------
sav='/home/zhenfeng/Research/GroupEvolution/src/code201611-MZ/sav/' 
US=loadData('userStates')
GS=loadData('groupStates')
NU=len(US)
Dir=sav+'Edgelists-all/'
fnames=os.listdir(Dir)
fileNames=[]
for f in fnames:
    if f.startswith('Edges'):
        fileNames.append(f)
fileNames=sorted(fileNames)
T=len(fileNames)
Ms={0:{},1:{},2:{}}
Path={0:{},1:{},2:{}}
t=0
for f in fileNames:
    fpath=Dir+f
    csvfile=open(fpath, 'rb')
    data = csv.reader(csvfile, delimiter=' ')
    for row in data:
        u=row[0]
        g=row[1]
        if not u in Ms[US[u]]:
            Ms[US[u]][u] = [t,T]
        else:
            Ms[US[u]][u][1] = t
        if g in GS:
            if not u in Path[US[u]]:Path[US[u]][u]=zeros(T)
            if GS[g] < 4:
                Path[US[u]][u][t]+=1.0
            if GS[g] >=4:
                Path[US[u]][u][t]-=1.0
    csvfile.close()
    del data

        
    t+=1

Ls={0:[],1:[],2:[]}
for i in Ms:
    for u in Ms[i]:
        if Ms[i][u][1] != T and Ms[i][u][0] !=T:
            Ls[i].append(Ms[i][u][1]-Ms[i][u][0]+1)
#---------------
t0 = 0

colors={0:'red',1:'green',2:'blue'}
labels={0:'banned',1:'alive',2:'deleted'}
f1=figure(1,figsize=(6,4))
for i in Ls:
    x,y=statistic(Ls[i],norm=True)
    _=loglog(x,y,color=colors[i],marker='o',linestyle='none',label=labels[i],alpha=0.5,ms=4)
P=[0.48,0.5,0.52]
for i in range(len(P)):
    _=loglog(x,fit(x,(2*P[i]-1.0),T),color=colors[i],linestyle='--',linewidth=2)
xlim([1,340])
ylim([1e-4,1e-1])
xlabel(r'Lifespan [day]')
ylabel(r'Fraction')
legend(loc='best')
f1.set_tight_layout(True)
savefig('figs/Lifespan-data-analytical.pdf', format='pdf')
close(1)

f=figure(1,figsize=(6,4))
for i in Path:
    f.clf()
    NU=1000
    for u in Path[i]:
        y=Path[i][u]
        if y[0]==0 and y[-1]==0:
            _=plot(y,alpha=0.2)
            NU-=1
        if NU<=0:break
    xlim([0,T])
    xlabel(r'$Time$')
    ylabel(r'$Position$')
    savefig('figs/Time-Position-data.png',bbox_inches='tight')
f.clf()
