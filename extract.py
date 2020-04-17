#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 17:33:55 2020

@author: sanyals
"""
import pickle
import numpy as np
import os
import torch


main_path = os.path.dirname(os.getcwd())
dataset = 'cifar10'
model = 'resnet18'
f = open('data/cifar-10-batches-py/test_batch','rb')
u = pickle._Unpickler(f)
u.encoding = 'latin1'
dict = u.load()
images = dict['data']
images = np.reshape(images, (10000, 3, 32, 32))
np.save('data/cifar10_inp',images)

weights = torch.load('data/' + dataset + '_' + model + '.pt')

convdic = {}

for k,v in weights.items():
    if 'conv' in k:
        convdic.update({k:v})
        
weight_path_name =  dataset + '_' + model + '_weights'       
        
if not os.path.exists(weight_path_name):
    os.makedirs('data/'+ weight_path_name)
             
        
for key,value in convdic.items():
    wt = value
    name = key[:-7]
    np.save('data/' + weight_path_name + '/' + name , wt)
    

    
