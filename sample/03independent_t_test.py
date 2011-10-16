#!/usr/bin/env python
# -*- mode: python -*- -*- coding: utf-8 -*-
import math
import os

import rpy2.robjects as robjects
from scipy import array, loadtxt
from scipy.stats import ttest_ind, t

from mystat import Stat, readcsv, t_distribution

DATA_PATH = os.path.join('data', 'h04_01.csv')
r = robjects.r

def calc():
    # read data
    data = readcsv(DATA_PATH)
    d0 = [x[1] for x in data]
    d1 = [x[2] for x in data]

    # calculation
    s0 = Stat(d0)
    s1 = Stat(d1)
    variance_estimation = (s0.variance*s0.size+s1.variance*s1.size)/((s0.size-1)+(s1.size-1))
    standard_error = math.sqrt(variance_estimation*((1.0/s0.size)+(1.0/s1.size)))
    df = (s0.size - 1) + (s1.size - 1)
    t_dist = t_distribution(df, alpha=0.05)
    t_dist_001 = t_distribution(df, alpha=0.01)
    diff_mean = s0.mean - s1. mean
    confidence_interval = (diff_mean-standard_error*t_dist,
                           diff_mean+standard_error*t_dist)
    t_value = diff_mean / standard_error

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
    r("out<-t.test(%s[,1], %s[,2], var.equal=F)" % (dataf.r_repr(),
                                                    dataf.r_repr()))

    # omake
    df = int(round(r("out$parameter")[0]))
    confidence_interval = (r("out$conf.int[1]")[0], r("out$conf.int[2]")[0])
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
    t_value, p_value = ttest_ind(data[:,0], data[:,1])

    # omake
    df = (data.shape[0] - 1) * data.shape[1]
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
