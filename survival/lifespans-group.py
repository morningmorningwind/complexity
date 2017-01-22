import os
import csv
from pylab import *
from numpy import *
import pickle
from itertools import cycle
from mymath import statistic,revcumsum,sortxy,rmean,readCSV
from random import sample as spl
import powerlaw as plw
from scipy.stats import weibull_min
from truncatedweilbull import TruWeil
#load the Groups of joining events
G={}
fpath=u'../../data/gids.csv'
csvfile=open(fpath, 'rt')
data = csv.reader(csvfile, delimiter=',')
i=0
for row in data:
    for j in row:
        G[j]=i
        i+=1
del data
csvfile.close()
del csvfile
           
NG=len(G)

#read the # of user data day by day
# get the file paths
Dir='../../data/Edgelists-all/'
fnames=os.listdir(Dir)
fileNames=[]
for f in fnames:
    if f.startswith('Edges'):
        fileNames.append(f)
fileNames=sorted(fileNames)

T=len(fileNames)
GS=zeros([NG,T])#group size vs t
t=0
for f in fileNames:
    fpath=Dir+f
    csvfile=open(fpath, 'rt')
    data = csv.reader(csvfile, delimiter=' ')
    for row in data:
        GS[G[row[1]],t]+=1.0
    del data
    csvfile.close()
    del csvfile
    t+=1

L=[]#life span
S=[]#group size
Idx0=zeros(GS.shape[0])

for i in range(GS.shape[0]):
    cnt=0.0
    gs=0.0
    flg=False
    for j in range(GS.shape[1]):
        if GS[i,j]>0:
            cnt+=1.0
            gs+=GS[i,j]
            if flg==False:
                Idx0[i]=j
                flg=True
        if GS[i,j]==0 or (j>=GS.shape[1]-1):
            if cnt>0:
                L.append(cnt)
                S.append(gs/cnt)
            cnt=0.0
            gs=0.0

L=readCSV('groupLifespan.txt','sav/')
for i in range(len(L)):
    L[i]=float(L[i][1])
#null model, random cuts
L1=[]#life span
p=1.0/mean(L)
s=mean(L)
for rep in range(10):
    GS1=ones([GS.shape[0],GS.shape[1]])
    ##for i in range(GS.shape[0]):
    ##    n0=len(where(GS[i,:]==0)[0])
    ##    idx=random.randint(0,GS.shape[1],n0)
    ##    GS1[i,idx]=0
    for i in range(GS1.shape[0]):
        idx0=Idx0[i]#random.randint(0,GS1.shape[1])
#        idx1=idx0+random.geometric(p)#
        idx1=random.randint(idx0,GS1.shape[1])
#        idx1=idx0+random.exponential(s)
        if idx0>=0:
            GS1[i,0:idx0]=0
        if idx1<GS1.shape[1]:
            GS1[i,idx1:]=0
    for i in range(GS1.shape[0]):
        cnt=0
        for j in range(GS1.shape[1]):
            if GS1[i,j]>0:
                cnt+=1.0
            if GS1[i,j]==0 or (j>=GS1.shape[1]-1):
                if cnt>0:
                    L1.append(cnt)
                cnt=0
                
f1=figure(1,figsize=(6,4))
f1.clf()
L=array(L,dtype=float)
L1=array(L1,dtype=float)
fit1=plw.Fit(L,xmin=1,xmax=100,discrete=True)
a=weibull_min.fit(L)
ax1=fit1.plot_pdf(original_data=True,color='k',label='empirical data')
#fit1.power_law.plot_pdf(ax=ax1,color='r',linestyle='--',linewidth=2,label=r'fitting: $\alpha='+('%.3f' % fit1.power_law.alpha)+'$')
x=linspace(1.5,330.0,1000)
ax1.loglog(x,weibull_min.pdf(x,*a),color='r',linestyle='--',linewidth=2,label=r'fitting:$\alpha='+str(round(a[0],3))+'$')
fit2=plw.Fit(L1,xmin=1,xmax=100,discrete=True)
fit2.plot_pdf(ax=ax1,original_data=True,color='lime',linestyle='-.',linewidth=2,label='null model')
xlabel(r'Life Span [day]')
ylabel(r'PDF')
ylim([1e-4,1])
legend(loc='best')
f1.set_tight_layout(True)
savefig('figs/lifespan-PDF-groups.pdf', format='pdf')          


f1=figure(1,figsize=(6,4))
f1.clf()
L=array(L,dtype=float)
L1=array(L1,dtype=float)
fit1=plw.Fit(L,xmin=1,xmax=100,discrete=True)
a=TruWeil(L)
afit=a.fit()
pdf=afit['pdf']
beta=afit['beta']
eta=afit['eta']
ax1=fit1.plot_pdf(original_data=True,color='k',label='empirical data')
#fit1.power_law.plot_pdf(ax=ax1,color='r',linestyle='--',linewidth=2,label=r'fitting: $\alpha='+('%.3f' % fit1.power_law.alpha)+'$')
x=linspace(1.5,330.0,1000)
ax1.loglog(x,pdf(x),color='r',linestyle='--',linewidth=2,label=r'fitting:$\beta='+str(round(beta,3))+', '+'\eta='+str(round(eta,3))+'$')
fit2=plw.Fit(L1,xmin=1,xmax=100,discrete=True)
fit2.plot_pdf(ax=ax1,original_data=True,color='lime',linestyle='-.',linewidth=2,label='null model')
xlabel(r'Life Span [day]')
ylabel(r'PDF')
ylim([1e-4,1])
legend(loc='best')
f1.set_tight_layout(True)
savefig('figs/lifespan-PDF-truncatedWeilbull-groups.pdf', format='pdf') 


f1.clf()
S=array(S,dtype=float)
x,y=sortxy(S,L)
plot(x,y,'s-')
xscale('log')
ylabel(r'Life Span [day]')
xlabel(r'Size')
legend(loc='best')
f1.set_tight_layout(True)
savefig('figs/lifespan-vs-size-groups.pdf', format='pdf') 

