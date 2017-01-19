from pylab import *
from numpy import *
from random import sample as rand_sample
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from scipy.interpolate import interp1d
from scipy.interpolate import griddata
from matplotlib import cm
import os
import csv
import time

def indsort(arr,reverse=False):
    return sorted(range(len(arr)),key=lambda z:arr[z],reverse=reverse)


def rebin(arr,xarr=None,bins=4,kind='linear'):
    valid_idx=where(isfinite(arr))
    if type(xarr)== type(None):
        x=arange(size(arr))
    else:
        x=copy(xarr)
    y=arr[valid_idx]
    x=x[valid_idx]
    Y=interp1d(x, y, kind=kind)
    x1=linspace(x.min(),x.max(),bins)
    y1=Y(x1)
    return x1,y1

def binned(arr,xarr=None,bins=10,mode='mean'):
    Mode={'mean':mean,'sum':sum}
    L=len(arr)
    L=L+bins-mod(L,bins)
    x,y=rebin(arr,xarr=xarr,bins=L)
    dm=L//bins
    x1=[mean(x[i:i+dm]) for i in arange(bins)*dm]
    y1=[Mode[mode](y[i:i+dm]) for i in arange(bins)*dm]
    return array(x1,dtype=float),array(y1,dtype=float)

def rmean(arr):
    return cumsum(arr)/arange(1,arr.size+1)

def statistic(List,norm=False):
    Uniq=unique(List[:])
    Num=[]
    if len(shape(List))==1:
        lst=List[:]
    else:
        lst=[x for i in List for x in i]
    for n in Uniq:
        Num.append(lst.count(n))
    Num=array(Num)
    if norm:Num=Num/float(sum(Num))
    return sortxy(Uniq,Num,as_array=True)

def countall(lst,norms=False):
    uniq=set(lst)
    cnt={}
    lscnt=lst.count
    if norms==True:
        num=float(len(lst))
        for i in uniq:
            cnt[i]=lscnt(i)/num
    else:
        for i in uniq:
            cnt[i]=lscnt(i)
    return cnt


def normalize(a,axis=0):
    sp=a.shape
    sz=sp[axis]
    One=ones([sz,sz])
    b=a.swapaxes(axis,a.ndim-1)
    Sum=tensordot(b,One,(b.ndim-1,0)).swapaxes(axis,b.ndim-1)
    return a/(Sum + 1e-50)

def dictsort(x,reverse=False):
    import operator
    sorted_x = sorted(x.iteritems(), key=operator.itemgetter(1),reverse=reverse)
    return sorted_x

def revcumsum(a,norm=False):
    res=cumsum(a[::-1])[::-1]
    if norm:res=res/float(res[0])
    return res

def sortxy(x,y,axis=0,as_array=True,**kwargs):
    # order x first, and then order y according to x
    xy=zip(x,y)
    xy=sorted(xy,key=lambda p:p[axis],**kwargs)
    x1,y1=zip(*xy)
    if as_array:
        return array(x1),array(y1)
    else:
        return list(x1), list(y1)


def savCSV(data,fname,path='',mode='wb',delimiter=',',quotechar='"'):
    if len(path)>0:
        if path[-1]!='/':
            path=path+'/'
    if fname[0]=='/':
        fname=fname[1:]
    if not os.path.exists(path):
        os.makedirs(path)
    savefname=path+fname
    csvfile=open(savefname, mode)
    w = csv.writer(csvfile, delimiter=delimiter,quotechar=quotechar,quoting=csv.QUOTE_MINIMAL)
    w.writerows(data)
    csvfile.close()
    del csvfile
    del w

def readCSV(fname,path='',mode='rb',delimiter=',',func=None):
    if len(path)>0:
        if path[-1]!='/':
            path=path+'/'
    if fname[0]=='/':
        fname=fname[1:]
    readfname=path+fname
    csvfile=open(readfname, mode)
    data = csv.reader(csvfile, delimiter=delimiter)
    res=[]
    for row in data:
        res.append(map(func,row))
    del data
    csvfile.close()
    del csvfile    
    return res
    
def fix2d(M,missing=nan,method='linear'):
    if missing!=missing:
        points=where(isfinite(M))
    else:
        points=where(M!=missing * isfinite(M))
    values=M[points]
    grid_x, grid_y = meshgrid(arange(M.shape[0]),arange(M.shape[1]))
    return griddata(points,values, (grid_x, grid_y), method=method).T
    
def surfplot(X,Y,Z,fname='',missing=nan,xlabel='x',ylabel='y',zlabel='z',proj=False,precision=50):
    X=array(X)
    Y=array(Y)
    Z=array(Z.T)
    X,Y=meshgrid(X,Y)
    Z=fix2d(Z,missing=missing)
    values=Z[isfinite(Z)]
    vmin=values.min()
    vmax=values.max()
    print(vmin)
    print(vmax)
    del values
    fig = figure()
    ax = fig.gca(projection='3d')
    surf=ax.plot_surface(X, Y, Z, cmap=cm.jet,vmin=vmin,vmax=vmax, linewidth=0,cstride=int(Z.shape[1]/precision),rstride=int(Z.shape[0]/precision), antialiased=False,alpha=0.8)
    if proj:
        cset = ax.contourf(X, Y, Z, zdir='z', offset=vmax,cmap=cm.jet,alpha=0.5)
#        cset = ax.contourf(X, Y, Z, zdir='x', offset=X.min(),cmap=cm.jet,alpha=0.5)
#        cset = ax.contourf(X, Y, Z, zdir='y', offset=Y.min(),cmap=cm.jet,alpha=0.5)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    fig.colorbar(surf, shrink=0.5)
    if fname != '':
        fig.set_tight_layout(True)
        savefig(fname, format='pdf')
        close(fig)

class wsample:
    def __init__(self,D):#D is the dictionary, whose keys are rvs, and values are weights
        self.probs=[]
        self.keys={}
        nk=0
        for k in D:
            self.probs.append(D[k])
            self.keys[nk]=k
            nk+=1
        self.probs=array(self.probs,dtype=float)
        self.probs=self.probs/self.probs.sum()
        self.setup()
    def setup(self):
        K       = len(self.probs)
        q       = zeros(K)
        J       = zeros(K, dtype=int)
     
        # Sort the data into the outcomes with probabilities
        # that are larger and smaller than 1/K.
        smaller = []
        larger  = []
        for kk, prob in enumerate(self.probs):
            q[kk] = K*prob
            if q[kk] < 1.0:
                smaller.append(kk)
            else:
                larger.append(kk)
     
        # Loop though and create little binary mixtures that
        # appropriately allocate the larger outcomes over the
        # overall uniform mixture.
        while len(smaller) > 0 and len(larger) > 0:
            small = smaller.pop()
            large = larger.pop()
     
            J[small] = large
            q[large] = q[large] + q[small] - 1.0
     
            if q[large] < 1.0:
                smaller.append(large)
            else:
                larger.append(large)
     
        self.J=J
        self.q=q
     
    def draw(self):
        K  = len(self.J)
     
        # Draw from the overall uniform mixture.
        kk = int(floor(random.rand()*K))
     
        # Draw from the binary mixture, either keeping the
        # small one, or choosing the associated larger one.
        
        if rand() < self.q[kk]:
            return self.keys[kk]
        else:
            return self.keys[self.J[kk]]
    def spl(self,n,timing=False):
        if timing:tic=time.time()
        # Generate variates.
        X =[]
        for nn in xrange(n):
            X.append(self.draw())
        
        if timing:print('time elapsed:'+str(time.time()-tic))
        return X
        
