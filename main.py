#! usr/bin/env python3#! usr/bin/env python3

import math
import csv
import itertools as it

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
from scipy.optimize import minimize
from scipy.stats import norm

from exergy.py import turbofan_analysis
