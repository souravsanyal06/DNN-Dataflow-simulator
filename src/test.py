#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 12:03:25 2020

@author: sanyals
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import random as r

from Mem import *


def stride_conv(arr1,arr2,s):
    
    arr1 = np.array([ [ [o.value for o in i] for i in j] for j in arr1])
    arr2 = np.array([ [ [ [o.value for o in i] for i in j] for j in k] for k in arr2])
    
    Cout = arr2.shape[1]
#    Cin = arr1.shape[0]
#    W = arr1.shape[1]
#    H = arr1.shape[2]
    
#    arr1 = np.zeros((Cin, W + 2*p, H + 2*p ))
#    
#    for i in range(Cin):
#        arr1[i][p:W+p,p:H+p] = arr1_[i]
#        
    #import pdb; pdb.set_trace()    
    
    assert arr1.shape[0] == arr2.shape[0] , "Input Channel dimension inconsistent across input and filter tensors"
        
    final = [ [] for i in range(0,Cout)]
      
    for op_ch in range(0,Cout):
        Cin = arr2.shape[0]
        out = [ [] for i in range(0, Cin)] 
        for c in range(0, Cin):
            beg_ = 0
            end_ = arr2[c][op_ch].shape[0]
            for i in range(0,arr1[c].shape[0]-2,s):
                k = []
                for j in range(0,arr1[c].shape[0]-2,s):
                    #import pdb; pdb.set_trace()
                    i_mat = arr1[c][beg_+i:end_+i, beg_+j:end_+j]
                    w_mat = arr2[c][op_ch]
                    psum = 0
                           
                    for i_ in range(end_):
                        for j_ in range(end_):
                            psum += i_mat[i_,j_]*w_mat[i_,j_]
                    k.append(psum)        
                    #k.append(np.sum(arr1[c][beg+i : end+i, beg+j:end+j] * (arr2[c][op_ch])))
                out[c].append(k)
        out = np.array(out)
        out_act = np.zeros((out.shape[1], out.shape[2]))
    
        for i in range(out.shape[0]):
            out_act += out[i] 
                 
        final[op_ch] = out_act.tolist()        
        
   
    return np.array(final)


#inp = np.array( [ [ [ r.random() for i in range(31)] for j in range(31)] for k in range (128)])
#filt = np.array( [ [ [ [r.random() for i in range(3)] for j in range(3)] for k in range (256)] for l in range (128)])
#es = stride_conv(inp,filt,1,1)
#
#print(res)