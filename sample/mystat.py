#!/usr/bin/env python
# -*- mode: python -*- -*- coding: utf-8 -*-

__author__ = "Sumiya 'higebobo' Sakoda"
__version__ = "$Revision: 1.1 $"
__date__ = "$Date: 2011/08/29 07:52:44 $"

import csv
import math
import os
import sys

T_DISTRIBUTION = {
    1: (12.706, 63.657),
    2: (4.303, 9.925),
    3: (3.182, 5.841),
    4: (2.776, 4.604),
    5: (2.571, 4.032),
    6: (2.447, 3.707),
    7: (2.365, 3.499),
    8: (2.306, 3.355),
    9: (2.262, 3.25),
    10: (2.226, 3.169),
    11: (2.201, 3.106),
    12: (2.179, 3.055),
    13: (2.16, 3.021),
    14: (2.145, 2.977),
    15: (2.131, 2.947),
    16: (2.12, 2.921),
    17: (2.11, 2.898),
    18: (2.101, 2.878),
    19: (2.093, 2.861),
    20: (2.086, 2.845),
    21: (2.08, 2.831),
    22: (2.074, 2.819),
    23: (2.069, 2.807),
    24: (2.064, 2.797),
    25: (2.06, 2.787),
    26: (2.056, 2.779),
    27: (2.052, 2.771),
    28: (2.048, 2.763),
    29: (2.045, 2.756),
    30: (2.042, 2.75),
    40: (2.021, 2.704),
    60: (2.0, 2.66),
    120: (1.98, 2.617),
    121: (1.96, 2.576),
}

F_DISTRIBUTION_005 = {
    1: (161.4, 199.5, 215.7, 224.6, 230.2, 234.0, 236.8, 238.9, 240.5, 241.9),
    2: (18.51, 19.00, 19.16, 19.25, 19.30, 19.33, 19.35, 19.37, 19.38, 19.40),
    3: (10.13, 9.552, 9.277, 9.117, 9.013, 8.941, 8.887, 8.845, 8.812, 8.786),
    4: (7.709, 6.944, 6.591, 6.388, 6.256, 6.163, 6.094, 6.041, 5.999, 5.964),
    5: (6.608, 5.786, 5.409, 5.192, 5.050, 4.950, 4.876, 4.818, 4.772, 4.735),
    6: (5.987, 5.143, 4.757, 4.534, 4.387, 4.284, 4.207, 4.147, 4.099, 4.060),
    7: (5.591, 4.737, 4.347, 4.120, 3.972, 3.866, 3.787, 3.726, 3.677, 3.637),
    8: (5.318, 4.459, 4.066, 3.838, 3.687, 3.581, 3.500, 3.438, 3.388, 3.347),
    9: (5.117, 4.256, 3.863, 3.633, 3.482, 3.374, 3.293, 3.230, 3.179, 3.137),
    10: (4.965, 4.103, 3.708, 3.478, 3.326, 3.217, 3.135, 3.072, 3.020, 2.978),
    11: (4.844, 3.982, 3.587, 3.357, 3.204, 3.095, 3.012, 2.948, 2.896, 2.854),
    12: (4.747, 3.885, 3.490, 3.259, 3.106, 2.996, 2.913, 2.849, 2.796, 2.753),
    13: (4.667, 3.806, 3.411, 3.179, 3.025, 2.915, 2.832, 2.767, 2.714, 2.671),
    14: (4.600, 3.739, 3.344, 3.112, 2.958, 2.848, 2.764, 2.699, 2.646, 2.602),
    15: (4.543, 3.682, 3.287, 3.056, 2.901, 2.790, 2.707, 2.641, 2.588, 2.544),
    16: (4.494, 3.634, 3.239, 3.007, 2.852, 2.741, 2.657, 2.591, 2.538, 2.494),
    17: (4.451, 3.592, 3.197, 2.965, 2.810, 2.699, 2.614, 2.548, 2.494, 2.450),
    18: (4.414, 3.555, 3.160, 2.928, 2.773, 2.661, 2.577, 2.510, 2.456, 2.412),
    19: (4.381, 3.522, 3.127, 2.895, 2.740, 2.628, 2.544, 2.477, 2.423, 2.378),
    20: (4.351, 3.493, 3.098, 2.866, 2.711, 2.599, 2.514, 2.447, 2.393, 2.348),
    21: (4.325, 3.467, 3.072, 2.840, 2.685, 2.573, 2.488, 2.420, 2.366, 2.321),
    22: (4.301, 3.443, 3.049, 2.817, 2.661, 2.549, 2.464, 2.397, 2.342, 2.297),
    23: (4.279, 3.422, 3.028, 2.796, 2.640, 2.528, 2.442, 2.375, 2.320, 2.275),
    24: (4.260, 3.403, 3.009, 2.776, 2.621, 2.508, 2.423, 2.355, 2.300, 2.255),
    25: (4.242, 3.385, 2.991, 2.759, 2.603, 2.490, 2.405, 2.337, 2.282, 2.236),
    26: (4.225, 3.369, 2.975, 2.743, 2.587, 2.474, 2.388, 2.321, 2.265, 2.220),
    27: (4.210, 3.354, 2.960, 2.728, 2.572, 2.459, 2.373, 2.305, 2.250, 2.204),
    28: (4.196, 3.340, 2.947, 2.714, 2.558, 2.445, 2.359, 2.291, 2.236, 2.190),
    29: (4.183, 3.328, 2.934, 2.701, 2.545, 2.432, 2.346, 2.278, 2.223, 2.177),
    30: (4.171, 3.316, 2.922, 2.690, 2.534, 2.421, 2.334, 2.266, 2.211, 2.165),
    40: (4.085, 3.232, 2.839, 2.606, 2.449, 2.336, 2.249, 2.180, 2.124, 2.077),
    60: (4.001, 3.150, 2.758, 2.525, 2.368, 2.254, 2.167, 2.097, 2.040, 1.993),
    120: (3.920, 3.072, 2.680, 2.447, 2.290, 2.175, 2.087, 2.016, 1.959, 1.910),
    121: (3.842, 2.997, 2.606, 2.373, 2.215, 2.099, 2.011, 1.939, 1.881, 1.832),
}

F_DISTRIBUTION_001 = {
    1: (4052.0, 4999.0, 5403.0, 5625.0, 5764.0, 5859.0, 5928.0, 5981.0, 6022.0, 6056.0),
    2: (98.50, 99.00, 99.17, 99.25, 99.30, 99.33, 99.36, 99.37, 99.39, 99.40),
    3: (34.12, 30.82, 29.46, 28.71, 28.24, 27.91, 27.67, 27.49, 27.35, 27.23),
    4: (21.20, 18.00, 16.69, 15.98, 15.52, 15.21, 14.98, 14.80, 14.66, 14.55),
    5: (16.26, 13.27, 12.06, 11.39, 10.97, 10.67, 10.46, 10.29, 10.16, 10.05),
    6: (13.75, 10.92, 9.780, 9.148, 8.746, 8.466, 8.260, 8.102, 7.976, 7.874),
    7: (12.25, 9.547, 8.451, 7.847, 7.460, 7.191, 6.993, 6.840, 6.719, 6.620),
    8: (11.26, 8.649, 7.591, 7.006, 6.632, 6.371, 6.178, 6.029, 5.911, 5.814),
    9: (10.56, 8.022, 6.992, 6.422, 6.057, 5.802, 5.613, 5.467, 5.351, 5.257),
    10: (10.04, 7.559, 6.552, 5.994, 5.636, 5.386, 5.200, 5.057, 4.942, 4.849),
    11: (9.646, 7.206, 6.217, 5.668, 5.316, 5.069, 4.886, 4.744, 4.632, 4.539),
    12: (9.330, 6.927, 5.953, 5.412, 5.064, 4.821, 4.640, 4.499, 4.388, 4.296),
    13: (9.074, 6.701, 5.739, 5.205, 4.862, 4.620, 4.441, 4.302, 4.191, 4.100),
    14: (8.862, 6.515, 5.564, 5.035, 4.695, 4.456, 4.278, 4.140, 4.030, 3.939),
    15: (8.683, 6.359, 5.417, 4.893, 4.556, 4.318, 4.142, 4.004, 3.895, 3.805),
    16: (8.531, 6.226, 5.292, 4.773, 4.437, 4.202, 4.026, 3.890, 3.780, 3.691),
    17: (8.400, 6.112, 5.185, 4.669, 4.336, 4.102, 3.927, 3.791, 3.682, 3.593),
    18: (8.285, 6.013, 5.092, 4.579, 4.248, 4.015, 3.841, 3.705, 3.597, 3.508),
    19: (8.185, 5.926, 5.010, 4.500, 4.171, 3.939, 3.765, 3.631, 3.523, 3.434),
    20: (8.096, 5.849, 4.938, 4.431, 4.103, 3.871, 3.699, 3.564, 3.457, 3.368),
    21: (8.017, 5.780, 4.874, 4.369, 4.042, 3.812, 3.640, 3.506, 3.398, 3.310),
    22: (7.945, 5.719, 4.817, 4.313, 3.988, 3.758, 3.587, 3.453, 3.346, 3.258),
    23: (7.881, 5.664, 4.765, 4.264, 3.939, 3.710, 3.539, 3.406, 3.299, 3.211),
    24: (7.823, 5.614, 4.718, 4.218, 3.895, 3.667, 3.496, 3.363, 3.256, 3.168),
    25: (7.770, 5.568, 4.675, 4.177, 3.855, 3.627, 3.457, 3.324, 3.217, 3.129),
    26: (7.721, 5.526, 4.637, 4.140, 3.818, 3.591, 3.421, 3.288, 3.182, 3.094),
    27: (7.677, 5.488, 4.601, 4.106, 3.785, 3.558, 3.388, 3.256, 3.149, 3.062),
    28: (7.636, 5.453, 4.568, 4.074, 3.754, 3.528, 3.358, 3.226, 3.120, 3.032),
    29: (7.598, 5.420, 4.538, 4.045, 3.725, 3.499, 3.330, 3.198, 3.092, 3.005),
    30: (7.562, 5.390, 4.510, 4.018, 3.699, 3.473, 3.304, 3.173, 3.067, 2.979),
    40: (7.314, 5.179, 4.313, 3.828, 3.514, 3.291, 3.124, 2.993, 2.888, 2.801),
    60: (7.077, 4.977, 4.126, 3.649, 3.339, 3.119, 2.953, 2.823, 2.718, 2.632),
    120: (6.851, 4.787, 3.949, 3.480, 3.174, 2.956, 2.792, 2.663, 2.559, 2.472),
    121: (6.637, 4.607, 3.784, 3.321, 3.019, 2.804, 2.641, 2.513, 2.409, 2.323),
}

class StatError(Exception):
    '''Stat Error class.'''
    
    def __init__(self, value='Stat Error'):
        if value:
            self.value = value

    def __str__(self):
        return repr(self.value)

class Stat(object):
    '''Calculate basically statistics value class.'''
    
    def __init__(self, data):
        self.size = len(data)
        self.total = sum(data)
        self.mean = self.total / self.size
        self.sum_of_squares = sum(((x-self.mean)**2 for x in data))
        self.variance = self.sum_of_squares / self.size
        self.standard_deviation = math.sqrt(self.variance)
        self.unbiased_variance = sum(((x-self.mean)**2 for x in data))/(self.size-1)
        self.standard_error = math.sqrt(self.unbiased_variance/self.size)

def t_distribution(df, alpha=0.05):
    '''\
    Calculate t distribution value (Dirty way ^^;).
    Parameters:
      * df: degree of freedom
      * alpha: significance level [0.05|0.01]
    Returns:
      * t distribution value
    See also:
      * http://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.t.html
      * http://www.evanjones.ca/statistics.py
    '''
    if df == 0:
        raise StatError('Degree must be above 0')
    elif df>30 and df<=35:
        df = 30
    elif df>35 and df<=50:
        df = 40
    elif df>50 and df<=90:
        df = 60
    elif df>90 and df<=120:
        df = 120
    elif df>=121:
        df = 121
    if alpha == 0.05:
        # 0.05
        index = 0
    else:
        # 0.01
        index = 1
    result = T_DISTRIBUTION.get(df)
    return result[index]

def F_distribution(df1, df2, alpha=0.05):
    '''\
    Calculate F distribution value (Dirty way ^^;).
    Parameters:
      * df1: degree of freedom 1
      * df2: degree of freedom 2
      * alpha: significance level [0.05|0.01]
    Returns:
      * F distribution value
    See also:
      * http://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.f.html
    '''

    if df1 > 10:
        raise StatError('This module support df1 <= 10.')
    if df2 == 0:
        raise StatError('Df2 must be above 0')
    elif df2>30 and df2<=35:
        df2 = 30
    elif df2>35 and df2<=50:
        df2 = 40
    elif df2>50 and df2<=90:
        df2 = 60
    elif df2>90 and df2<=120:
        df2 = 120
    elif df2>=121:
        df2 = 121
    if alpha == 0.05:
        # 0.05
        index = 0
    else:
        # 0.01
        index = 1    
    if alpha == 0.05:
        # 0.05
        table = F_DISTRIBUTION_005
    else:
        # 0.01
        table = F_DISTRIBUTION_001
    result = table.get(df2)
    return result[df1-1]

def linear_regression(x, y):
    '''\
    Calculate linear regression by least squares method.
    Require Stat class.
    Parameters:
      * x: explanatory variable
      * y: dependent variable
    Returns:
      * r: correlation coefficient
      * b: slope of the line
      * a: intercept
    '''
    x_s = Stat(x)
    y_s = Stat(y)
    x_sd = (a - x_s.mean for a in x)
    y_sd = (a - y_s.mean for a in y)
    z = [a[0]*a[1] for a in zip(x_sd, y_sd)]
    z_s = Stat(z)
    r = z_s.mean / (x_s.standard_deviation * y_s.standard_deviation)
    b = r * (y_s.standard_deviation / x_s.standard_deviation)
    a = y_s.mean - b * x_s.mean
    return r, a, b

def readcsv(csvfile, header=False):
    '''\
    Read from csv file.
    Parameters:
      * csvfile: csv format file path
      * header: flag that include the first row as a header (default False)
    Returns:
      * one-dimensional array (float data list)
    '''
    result = []
    fp = open(csvfile, 'r')
    rows = csv.reader(fp)
    for i, row in enumerate(rows):
        if not i:
            if header:
                result.append([x for x in row])
            continue
        result.append([float(x) for x in row])
    fp.close()
    return result

def main(argv):
    print 't-distribution value'
    for i in xrange(1, 124):
        print i, t_distribution(i)
    print 

    print 'F-distribution value'
    for i in xrange(1, 124):
        for j in xrange(1, 11):
            print i, j, F_distribution(j, i)
    print
    
if __name__ == "__main__":
    main(sys.argv)