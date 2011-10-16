#!/usr/bin/env python
# -*- mode: python -*- -*- coding: utf-8 -*-
import itertools
import math
import os

from matplotlib import pyplot as plt
from matplotlib import font_manager as fm
from numpy import loadtxt, vstack, ones, corrcoef
from numpy.linalg import lstsq
import rpy2.robjects as robjects

from mystat import Stat, readcsv, linear_regression

DATA_PATH = os.path.join('data', 'i01_04.csv')
r = robjects.r

def calc():
    # read data
    rawdata = readcsv(DATA_PATH)

    # pre-calculation
    x = [z[1] for z in rawdata]
    y = [z[2] for z in rawdata]
    
    # calculation
    cor, a, b = linear_regression(x, y)
    
    # output
    print '[Pure Python]'
    print 'Y = %f + %fX (r=%0.2f)' % (a, b, cor)
    print
    return x, y, a, b, cor
    
def calc_r():
    # read data
    dataf = r('read.csv("%s", header=T)' % DATA_PATH.replace('\\', '/'))

    # pre-calculation
    x = r('x<-%s[,2]' % dataf.r_repr())
    y = r('y<-%s[,3]' % dataf.r_repr())

    # calculation
    out = r('out<-lm(y~x)')
    out2 = r.cor(x, y)

    # output
    a = r('out$coefficients')[0]
    b = r('out$coefficients')[1]
    cor = out2[0]
    
    # output
    print '[R]'
    print 'Y = %f + %fX (r=%0.2f)' % (a, b, cor)
    print

def calc_numpy():
    # read data
    data = loadtxt(DATA_PATH, delimiter=",", skiprows=1, usecols=(1,2))

    # pre-calculation
    x = data[:, 0]
    y = data[:, 1]
    A = vstack((x, ones(len(x)))).T
    
    # calculation
    X, residues, rank, s = lstsq(A, y)
    cor = corrcoef(x, y)
    
    # output
    print '[Numpy]'
    print 'Y = %s + %sX (r=%0.2f)' % (X[1], X[0], cor[0][1])
    print

def plot_scatter(x, y):
    plt.scatter(x, y)
    plt.xlabel('distance from nearest station (m)')
    plt.ylabel('average number of customers (person)')
    plt.show()

def plot(x, y, a, b, cor):
    f = lambda x: a + b * x
    est = [f(z) for z in x]
    plt.plot(x, y, 'ko', label='real', markersize=8)
    plt.plot(x, est, '-', label='estimate ($Y=%f+%fX$, r=%0.2f)'%(a,b, cor))
    plt.legend(loc='upper right')
    plt.xlabel('distance from nearest station (m)')
    plt.ylabel('average number of customers (person)')
    plt.show()
    
if __name__ == '__main__':
    x, y, a, b, cor = calc()
    calc_r()
    calc_numpy()
    plot_scatter(x, y)
    plot(x, y, a, b, cor)
