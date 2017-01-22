# encoding: utf-8
import os
import csv
from pylab import *
from numpy import *
from loadData import loadData
from mymath import statistic, revcumsum
#read the data day by day
# get the file paths

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
loglog(x,y,'-')
xlim([1,340])
xlabel(r'Lifespan [day]')
ylabel(r'Fraction')
f1.set_tight_layout(True)
savefig('figs/Lifespan-bannedUsers-data.pdf', format='pdf')
close(1)
