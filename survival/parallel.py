from numpy import *
from multiprocessing import Pool
import time

def pfor(func,indices,mode='map',timing=True,np=None,mpc=1,*args,**kwargs):
    if timing: tic=time.time()
    if mode=='map':
        res=map(lambda x:func(x,*args,**kwargs),indices)
    if mode=='pmap':
        pool=Pool(np,maxtasksperchild=mpc)
#           res=pool.map(func,indices,**kwargs)
        res = pool.map_async(func,indices,**kwargs).get(9999999)
        pool.close()
        pool.join()
    if timing: toc=time.time()
    if timing: print 'Task runs %0.4f seconds.' % (toc-tic)
    return res

##def func1(i):
##    def func2(j):
##        Bij=A[i,:].dot(A[:,j])
##        return Bij
##    res=pfor(func2,range(num),timing=False)
##    return res   
##    
##
###if __name__=='__main__':
##num=1000
##A=random.randint(0,10,[num,num])
##B=zeros(A.shape)
##tic=time.time()
##for i in range(A.shape[0]):
##    for j in range(A.shape[1]):
##        B[i,j]=sum(A[i,:]*A[:,j])
##toc=time.time()
##print (toc-tic)
##print(B)
##tic=time.time()
##B=A.dot(A)
##toc=time.time()
##print(toc-tic)
##print(B)
##B=pfor(func1,range(num))
##print(array(B))
##B=pfor(func1,range(num),mode='pmap',A=A)
##print(array(B))
##    

            
        
        
