import numpy as np
import sys
import os
import random
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Data import *
import config 

class Mem:
    def __init__(self, ifmaps, weights,  Chnl_blk):

        #Reading layer parameters
#        lparams = {}
#        with open (layer_file) as layer:
#            for line in layer:
#                if  line.strip():
#                    params, val = line.partition("=")[::2]
#                    lparams[params.strip()]= int(val)

        self.Cout, self.Cin, self.Wf, self.Hf = weights.shape
       
        self.WI, self.HI = ifmaps[0].shape
        self.s = 1 #default
        self.p = 1  #default
#        self.batch_size = int(lparams["batch_size"])arr1 = np.zeros((self.Cin, self.WI + 2*self.p, self.HI + 2*self.p ))
    
        arr1 = np.zeros((self.Cin, self.WI + 2*self.p, self.HI + 2*self.p ))
        for i in range(self.Cin):
            arr1[i][self.p:self.WI+self.p,self.p:self.HI+self.p] = ifmaps[i]
            
        ifmaps = arr1
        
        
        
        self.WI = int(self.WI + 2*self.p)
        self.HI = int(self.HI + 2*self.p)
        
        
        self.WI_t = min(int(config.PE_width), self.WI)
        self.HI_t = min(int(config.PE_height), self.HI)
                  
        self.num_wt = int(math.ceil((self.WI)/config.PE_width))
        self.num_ht = int(math.ceil((self.HI)/config.PE_height))
        
        self.num_wt = self.WI  if self.num_wt == 1 else self.WI_t
        self.num_ht = self.HI  if self.num_ht == 1 else self.HI_t
        
               
        self.Co_b = int(Chnl_blk)
        
        self.Wo_t = int((self.WI_t - self.Wf)/self.s)+1
        self.Ho_t = int((self.HI_t - self.Hf)/self.s)+1
                
        
        if (self.WI_t < self.Wf) :   #for deeper layers
            self.p = 2
            self.s = 1
            self.WI_t = ifmaps.shape[1] + 2*self.p
            self.HI_t = ifmaps.shape[2] + 2*self.p
            
            self.Wo_t = int((self.WI_t - self.Wf)/self.s)+1
            self.Ho_t = int((self.HI_t - self.Hf)/self.s)+1
            
            
            arr1 = np.zeros((self.Cin, self.WI + 2*self.p, self.HI + 2*self.p ))
    
            for i in range(self.Cin):
                arr1[i][self.p:self.WI+self.p,self.p:self.HI+self.p] = ifmaps[i]
                
            ifmaps = arr1
            

        random.seed(7)

        self.wt = np.array( [ [ [ [Data(float(weights[k][l][j][i])) for i in range(self.Wf)] for j in range(self.Hf)] for k in range(self.Cout) ] for l in range(self.Cin)], dtype = object)
        print('Memory allocated in DRAM for weights')
        print(self.wt.shape)

        self.inp = np.array( [ [ [ Data(float(ifmaps[k][j][i])) for i in range(self.WI_t)] for j in range (self.HI_t)] for k in range(self.Cin) ], dtype = object)
        print('Memory allocated in DRAM for Inputs')
        print(self.inp.shape)
   
        
        self.ifmap = np.array( [ [ [ Data(float(ifmaps[k][j][i])) for i in range(self.WI_t)] for j in range (self.HI_t)] for k in range(self.Cin) ], dtype = object)
        
        


        





 


        

        

        
       



