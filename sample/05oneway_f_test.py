#!/usr/bin/env python
# -*- mode: python -*- -*- coding: utf-8 -*-
import itertools
import math
import os

import rpy2.robjects as robjects
from scipy import array, loadtxt
from scipy.stats import f_oneway
from scipy.stats import f

from mystat import Stat, readcsv, F_distribution

DATA_PATH = os.path.join('data', 'h06_02.csv')
r = robjects.r

def calc():
    # read data
    rawdata = readcsv(DATA_PATH)

    # calculation
    DATA = []
    S = []
    for i in xrange(0, len(rawdata[0])):
        d = [x[i] for x in rawdata]
        DATA.append(d)
        S.append(Stat(d))
    data = list(itertools.chain.from_iterable(DATA)) # flattend list from DATA 
    s = Stat(data)
    SUM_OF_SQUARES = sum((x.sum_of_squares for x in S))
    SS = [((x.mean-s.mean)**2)*x.size for x in S]
    ss = sum(SS)
    sum_of_squares = (ss, SUM_OF_SQUARES, s.sum_of_squares)
    degrees = (len(S)-1, sum([x.size-1 for x in S]), s.size-1)
    mean_squares = [sum_of_squares[i]/degrees[i] for i in (0, 1)]
    F_value = mean_squares[0] / mean_squares[1]
    F_dist = F_distribution(degrees[0], degrees[1])
    F_dist_001 = F_distribution(degrees[0], degrees[1], alpha=0.01)

    # output
    print '[Pure Python]'
    print 'F value:', F_value
    print 'F dist(0.05):', F_dist, abs(F_value)>F_dist
    print 'F dist(0.01):', F_dist_001, abs(F_value)>F_dist_001
    print 

def calc_r():
    # read data
    dataf = r('read.csv("%s", header=T)' % DATA_PATH.replace('\\', '/'))

    # pre-calculation
    r('n<-length(%s[,1])' % dataf.r_repr())
    r('a1<-%s[,1]' % dataf.r_repr())
    r('a2<-%s[,2]' % dataf.r_repr())
    r('a3<-%s[,3]' % dataf.r_repr())
    r('x<-data.frame(A=factor(c(rep("a1",n),rep("a2",n),rep("a3",n))), y=c(a1,a2,a3))')

    # calculation
    #r('x.aov<-aov(y~A,data=x)')
    #out = r('summary(x.aov)')
    out = r('out<-anova(aov(y~A,data=x))')
    print '[R]'
    print out
    print
    
    # omake
    df1 = r('out$Df')[0]
    df2 = r('out$Df')[1]
    F_value = r('out$F')[0]
    p_value = r('out$Pr')[0]
    F_dist = r.qf(0.95, df1, df2)[0]
    F_dist_001 = r.qf(0.99, df1, df2)[0]

    print '[R]'
    print 'F value:', F_value
    print 'p value:', p_value
    print 'F dist(0.05):', F_dist, abs(F_value)>F_dist
    print 'F dist(0.01):', F_dist_001, abs(F_value)>F_dist_001
    print 

def calc_scipy():
    # read data
    data = loadtxt(DATA_PATH, delimiter=",", skiprows=1)

    # calculation
    F_value, p_value = f_oneway(data[:,0], data[:,1], data[:,2])

    # omake
    df1 = data.shape[1] - 1
    df2 = data.shape[0] * data.shape[1] - data.shape[1]
    F_dist = f.ppf(0.95, df1, df2)
    F_dist_001 = f.ppf(0.99, df1, df2)

    # output
    print '[Scipy]'
    print 'F value:', F_value
    print 'p value:', p_value
    print 'F dist(0.05):', F_dist, abs(F_value)>F_dist
    print 'F dist(0.01):', F_dist_001, abs(F_value)>F_dist_001
    
if __name__ == '__main__':
    calc()
    calc_r()
    calc_scipy()
