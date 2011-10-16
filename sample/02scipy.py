#!/usr/bin/env python
# -*- mode: python -*- -*- coding: utf-8 -*-
from scipy import array, loadtxt

# read from csv
data = loadtxt('data/sample.csv', delimiter=",", skiprows=1,
               usecols=xrange(1,4))
print "[data]"
print data
print

# slice
# R -> data[2,]
mary = data[1]
print "[second row data]"
print mary
print

# R-> data[,1]
a = data[0, 0:]
print "[first column data]"
print a
print

# R-> data[1,2:3]
john_bc = data[1, 1:]
print "[first row,  second, third column data]"
print john_bc
print
