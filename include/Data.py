from __future__ import print_function


import numpy as np
from numpy import *


class Data:
    def __init__(self, value):
        self.value = value
        self.dense_count = 0
        self.sparse_count = 0

    def increment_densecount(self):
        self.dense_count += 1
        
    def increment_sparsecount(self):
        self.sparse_count += 1
 

