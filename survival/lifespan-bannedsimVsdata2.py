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

N = 200000 # number of users
T = 320
P = [0.48,0.5,0.52] # probability of joiningn a banned group
mxP = 10 # maximum cumulative position for banning

#randomize initial time for each user
T0 = random.randint(0,T,N)*0
P0 = random.randint(mxP-T,mxP,N).astype(int)
#P0 = (random.random(N)*100-90).astype(int)
#P0 = -(random.lognormal(0,10,N).astype(int)-3)
POS = []
LSP = []
POS0 = []
for p in P:
    Lsp = [] # life span
    #do simulation
    Pos=(random.random([N,T]) < p) * 2.0  -1.0
    for u in range(N):
        Pos[u,:T0[u]+1.0] = 0.0
        Pos[u,T0[u]] = P0[u]
    Pos = Pos.cumsum(1)
    Pos0 = []
    for u in range(N):
        if P0[u]<mxP:
            L = where(Pos[u,T0[u]+1:]>=mxP)[0]
            if len(L)>0:
                Lsp.append(L[0]+1)
                Pos0.append(P0[u])
                
    POS.append(Pos)
    LSP.append(Lsp)
    POS0.append(Pos0)
        

#data---------
US=loadData('userStates')
NU=len(US)
Dir='sav/Edgelists-all/'
fnames=os.listdir(Dir)
fileNames=[]
for f in fnames:
    if f.startswith('Edges'):
        fileNames.append(f)
fileNames=sorted(fileNames)
T=len(fileNames)
Ms={}
t=0
for f in fileNames:
    fpath=Dir+f
    csvfile=open(fpath, 'rb')
    data = csv.reader(csvfile, delimiter=' ')
    U=set()
    for row in data:
        if US[row[0]] == 0:
            U.add(row[0])
    csvfile.close()
    del data
    for u in U:
        if not u in Ms:
            Ms[u] = [t,T]
        else:
            Ms[u][1] = t
    t+=1

Ls=[]
for u in Ms:
    if Ms[u][1] != T and Ms[u][0] !=T:
        Ls.append(Ms[u][1]-Ms[u][0]+1)
#---------------
t0 = 0

f1=figure(1,figsize=(6,4))
x,y=statistic(Ls,norm=True)
_=loglog(x,y,color='purple',marker='o',linestyle='none',label='empirical',alpha=0.5,ms=4)
colors={0:'red',1:'green',2:'blue'}
for i in range(len(P)):
    Lsp=LSP[i]
    x,y=statistic(Lsp,norm=True)
    _=loglog(x,y,color=colors[i],label='$p$='+str(P[i]),alpha=0.5)
    _=loglog(x,fit(x,(2*P[i]-1.0),T),color=colors[i],linestyle='--',linewidth=2)
    
xlim([1,340])
ylim([1e-4,1e-1])
xlabel(r'Lifespan [day]')
ylabel(r'Fraction')
legend(loc='best')
f1.set_tight_layout(True)
savefig('figs/Lifespan-bannedUsers-data-vs-sim.pdf', format='pdf')
close(1)

f=figure(1,figsize=(6,4))
for i in range(len(P)):
    f.clf()
    Pos=POS[i]
    for u in range(100):
        y=Pos[u,:]
        y[:T0[u]]=nan
        _=plot(y,alpha=0.2)
#    _=plot([t0,t0],[100,-100],'r--',linewidth=2.0)
    _=plot([t0,t0+T],[mxP,mxP],'r--',linewidth=2.0)
    xlim([0,T])
    xlabel(r'$Time$')
    ylabel(r'$Position$')
    savefig('figs/Time-Position-sim-p'+str(P[i])+'.png',bbox_inches='tight')

f.clf()

for i in range(len(P)):
    Pos0=POS0[i]
    x,y=statistic(Pos0,norm=True)
    _=plot(x,y,label='$p$='+str(P[i]))

x,y=statistic(P0.tolist(),norm=True)
_=plot(x,y,label=r'$P(x,t_0)$')
xlabel(r'$Position$')
ylabel(r'$Fraction$')
legend(loc='best')
savefig('figs/InitialPosition-sim.pdf',bbox_inches='tight')
close(1)

