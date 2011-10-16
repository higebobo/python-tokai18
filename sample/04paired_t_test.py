#!/usr/bin/env python
# -*- mode: python -*- -*- coding: utf-8 -*-
import math
import os

import rpy2.robjects as robjects
from scipy import array, loadtxt
from scipy.stats import ttest_rel, t

from mystat import Stat, readcsv, t_distribution

DATA_PATH = os.path.join('data', 'h05_01.csv')
r = robjects.r

def calc():
    # read data
    data = readcsv(DATA_PATH)
    d = [x[1]-x[2] for x in data]

    # calculation
    s = Stat(d)
    df = s.size - 1
    t_dist = t_distribution(df, alpha=0.05)
    t_dist_001 = t_distribution(df, alpha=0.01)
    t_value = s.mean / s.standard_error

    # output
    print '[Pure Python]'
    print 't value:', t_value
    print 't dist(0.05):', t_dist, abs(t_value)>t_dist
    print 't dist(0.01):', t_dist_001, abs(t_value)>t_dist_001
    print 

def calc_r():
    # read data
    dataf = r('read.csv("%s", header=T, row.names=1)' % DATA_PATH.replace('\\', '/'))

    # calculation
    r("out<-t.test(%s[,1], %s[,2], paired = TRUE)" % (dataf.r_repr(),
                                                      dataf.r_repr()))

    # omake
    confidence_interval = (r("out$conf.int[1]")[0], r("out$conf.int[2]")[0])
    df = int(round(r("out$parameter")[0]))
    p = 0.05
    t_dist = r('qt(c(%s/2, %s/2 + (1-%s)), %s)' % (p, p, p, df))[1]
    p = 0.01
    t_dist_001 = r('qt(c(%s/2, %s/2 + (1-%s)), %s)' % (p, p, p, df))[1]
    
    # output
    t_value = r("out$statistic")[0]
    p_value = r("out$p.value")[0]
    print '[R]'
    print 't value:', t_value
    print 'p value:', p_value
    print 't dist(0.05):', t_dist, abs(t_value)>t_dist
    print 't dist(0.01):', t_dist_001, abs(t_value)>t_dist_001
    print 

def calc_scipy():
    # read data
    data = loadtxt(DATA_PATH, delimiter=",", skiprows=1, usecols=(1,2))

    # calculation
    t_value, p_value = ttest_rel(data[:,0], data[:,1])

    # omake
    df = data.shape[0] - 1
    t_dist = t.interval(0.95, df)
    t_dist_001 = t.interval(0.99, df)
    
    # output
    print '[Scipy]'
    print 't value:', t_value
    print 'p value:', p_value
    print 't dist(0.05):', t_dist[1], abs(t_value)>t_dist[1]
    print 't dist(0.01):', t_dist_001[1], abs(t_value)>t_dist_001[1]
    print 
    
if __name__ == '__main__':
    calc()
    calc_r()
    calc_scipy()
