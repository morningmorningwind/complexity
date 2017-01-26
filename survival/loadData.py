# encoding: utf-8
import os
import csv
from pylab import *
from numpy import *

def loadData(name):
#    DATADIR='sav/'
    DATADIR='/home/zhenfeng/Research/GroupEvolution/src/code201611-MZ/sav/' 
    if name == 'allGroups':
        G={}
        fpath=DATADIR+'gids-all.csv'
        csvfile=open(fpath, 'rb')
        data = csv.reader(csvfile, delimiter=',')
        i=0
        for row in data:
            for j in row:
                G[j]=i
                i+=1
        del data
        csvfile.close()
        del csvfile
        return G
    if name == 'joinGroups':
        G={}
        fpath=DATADIR+'gids-join.csv'
        csvfile=open(fpath, 'rb')
        data = csv.reader(csvfile, delimiter=',')
        i=0
        for row in data:
            for j in row:
                G[j]=i
                i+=1
        del data
        csvfile.close()
        del csvfile
        return G
    if name == 'groupStates':
        GS={}
        fpath=DATADIR+'GroupState.txt'
        csvfile=open(fpath, 'rb')
        data = csv.reader(csvfile, delimiter=',')
        for row in data:
            GS[row[0]]=int(row[1])
        del data
        csvfile.close()
        del csvfile
        return GS
    if name == 'avgGroupSizes':
        S={}
        fpath=DATADIR+'avgGroupSizes.txt'
        csvfile=open(fpath, 'rb')
        data = csv.reader(csvfile, delimiter=',')
        for row in data:
            S[row[0]]=float(row[1])
        del data
        csvfile.close()
        del csvfile
        return S
    if name == 'allUsers':
        U={}
        fpath=DATADIR+'uids-all.csv'
        csvfile=open(fpath, 'rb')
        data = csv.reader(csvfile, delimiter=',')
        i=0
        for row in data:
            for j in row:
                U[j]=i
                i+=1
        del data
        csvfile.close()
        del csvfile
        return U
    if name == 'joinUsers':
        U={}
        fpath=DATADIR+'uids-join.csv'
        csvfile=open(fpath, 'rb')
        data = csv.reader(csvfile, delimiter=',')
        i=0
        for row in data:
            for j in row:
                U[j]=i
                i+=1
        del data
        csvfile.close()
        del csvfile
        return U

    if name == 'userStates':
        UI={}
        csvfile=open(DATADIR+'UserState.txt', 'rb')
        data = csv.reader(csvfile, delimiter=',')
        for row in data:
            UI[row[0]]=int(row[1])
        del data
        csvfile.close()
        del csvfile
        return UI

    if name == 'groupsByDay':
        GBD={}
        fpath=DATADIR+'GroupsByDay.txt'
        csvfile=open(fpath, 'rb')
        data = csv.reader(csvfile, delimiter=',')
        for row in data:
            GBD[int(row[0])]=row[1:]
        del data
        csvfile.close()
        del csvfile
        return GBD

    if name == 'NJoinsByDay':
        JBD={}
        fpath=DATADIR+'NJoinsByDay.txt'
        csvfile=open(fpath, 'rb')
        data = csv.reader(csvfile, delimiter=',')
        for row in data:
            JBD[row[0]]=map(int,row[1:])
        del data
        csvfile.close()
        del csvfile
        return JBD
    print('dataNotFound!')

