#!/usr/bin/env python
# -*- mode: python -*- -*- coding: utf-8 -*-
import rpy2.robjects as robjects
r = robjects.r

# read from csv
data = r['read.csv']('data/sample.csv', header=False)
print "[data]"
print data
print

data = r('read.csv("data/sample.csv", header=T, row.names=1)')
print "[data]"
print data
print

# slice 1
mary = r('%s[2,]' % data.r_repr())
print "[second row data]"
print mary
print

# globalenv
try:
    renv = robjects.globalenv
except:
    renv = robjects.globalEnv
renv['data'] = data

print "[second row data]"
mary = r('data[2,]')
print mary
print

# vector
c = r('c(10, 20, 30)')
print "[vector]"
print c
print

c = robjects.IntVector([10, 20, 30])
print "[vector]"
print c
print

# slice 2
a = r('%s[,1]' % data.r_repr())
print "[first column data]"
print a
print

john_bc = r('%s[1,2:3]' % data.r_repr())
print "[first row,  second, third column data]"
print john_bc
print
