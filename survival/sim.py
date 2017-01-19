from pylab import *
from numpy import *
from mymath import statistic,revcumsum
N = 100000 # number of users
t0 = 500 # initial time for observation
T = t0 +1000
P = [0.45, 0.5, 0.55] # probability of joining a banned group
mxP = 5 # maximum cumulative position for banning

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
                Lsp.append(L-max(t0,T0[u]))
    POS.append(Pos)
    LSP.append(Lsp)
    POS0.append(Pos0)
        
f=figure(1,figsize=(6,4))
for i in range(len(P)):
    Lsp=LSP[i]
    x,y=statistic(Lsp,norm=True)
    _=loglog(x,y,label='$p$='+str(P[i]),alpha=0.5)
xlabel(r'$Lifespan$')
ylabel(r'$Fraction$')
legend(loc='best')
savefig('figs/lifespan-sim.pdf',bbox_inches='tight')


for i in range(len(P)):
    f.clf()
    Pos=POS[i]
    for u in range(300):
        _=plot(Pos[u,:],alpha=0.5)
    _=plot([t0,t0],[100,-100],'r--',linewidth=2.0)
    _=plot([t0,T],[mxP,mxP],'r--',linewidth=2.0)
    xlabel(r'$Time$')
    ylabel(r'$Position$')
    savefig('figs/Time-Position-sim-p'+str(P[i])+'.png',bbox_inches='tight')

f.clf()
for i in range(len(P)):
    Pos0=POS0[i]
    x,y=statistic(Pos0,norm=True)
    _=loglog(x,y,label='$p$='+str(P[i]),alpha=0.5)
xlabel(r'$Position$')
ylabel(r'$Fraction$')
legend(loc='best')
savefig('figs/InitialPosition-sim.pdf',bbox_inches='tight')
close(1)
