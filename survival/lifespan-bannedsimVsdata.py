# encoding: utf-8
import os
import csv
from pylab import *
from numpy import *
from loadData import loadData
from mymath import statistic, revcumsum
from random import sample as spl
#sim
N = 200000 # number of users
t0 = 500 # initial time for observation
T = t0 +320
P = [0.52] # probability of joining a banned group
mxP = 2 # maximum cumulative position for banning

#randomize initial time for each user
T0 = random.randint(0,t0,N)

POS = []
LSP = []
POS0 = []
for p in P:
    Pos = zeros([N,T]) # position vs time for each user
    Lsp = [] # life span
    #do simulation
    Pos[:,1:] = (random.random([N,T-1]) < p) * 2.0  - 1.0
    for u in range(N):
        Pos[u,:T0[u]+1] = 0.0 
    Pos = Pos.cumsum(1)
    Pos0 = Pos[t0,:].tolist()

    for u in range(N):
        L = where(Pos[u,:]>=mxP)[0]
        if len(L)>0:
            L=L[0]
            if L>t0:
                Lsp.append(L-max(T0[u],t0))
    POS.append(Pos)
    LSP.append(Lsp)
    POS0.append(Pos0)
        

#data
US=loadData('userStates')
N=len(US)
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
    if Ms[u][1] != T:
        Ls.append(Ms[u][1]-Ms[u][0]+1)

f1=figure(1,figsize=(6,4))
x,y=statistic(Ls,norm=True)
_=loglog(x,y,'ro',label='empirical',alpha=0.5)

Lsp=LSP[0]
x,y=statistic(Lsp,norm=True)
_=loglog(x,y,'g-',label='$p$='+str(P[0]),alpha=0.5)
xlim([1,330])
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
    for u in range(500):
        _=plot(Pos[u,:],alpha=0.2)
    _=plot([t0,t0],[100,-100],'w--',linewidth=2.0)
    _=plot([t0,t0+T],[mxP,mxP],'w--',linewidth=2.0)
    xlabel(r'$Time$')
    ylabel(r'$Position$')
    savefig('figs/Time-Position-sim-p'+str(P[i])+'.png',bbox_inches='tight')

f.clf()

for i in range(len(P)):
    Pos0=POS0[i]
    x,y=statistic(Pos0,norm=True)
    _=plot(x,y,label='$p$='+str(P[i]))

xlabel(r'$Position$')
ylabel(r'$Fraction$')
legend(loc='best')
savefig('figs/InitialPosition-sim.pdf',bbox_inches='tight')
close(1)

