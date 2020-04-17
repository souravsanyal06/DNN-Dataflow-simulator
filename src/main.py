import numpy as np
import sys
import os
import argparse
import configparser
import math
import pandas as pd
import collections 

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_dir = os.path.join(root_dir, "src")
include_dir = os.path.join(root_dir, "include")
results_dir = os.path.join(root_dir, "results")

sys.path.insert(0, root_dir)
sys.path.insert(0, src_dir)
sys.path.insert(0, include_dir)
sys.path.insert(0, results_dir)

from Mem import *
from config import *
from Istation import *
from Wstation import *
from Ostation import *
from visualize import *
from test import *


def relu(x):
    return np.maximum(x,0)


def collect_stats(blist, file):
    dic = {i : [] for i in blist}
    keys = list(dic.keys())
    IS = []
    WS = []
    OS = []
    with open(file) as f:
        for line in f:
            if 'Input Stationary Reduction' in line:
                IS.append(float(line.split()[-1]))
            if 'Weight Stationary Reduction' in line:
                WS.append(float(line.split()[-1]))
            if 'Output Stationary Reduction' in line:
                OS.append(float(line.split()[-1]))    
     
    for i in range(len(keys)):
        dic[keys[i]].append(IS[i])
        dic[keys[i]].append(WS[i])
        dic[keys[i]].append(OS[i])
        
    return dic
        


class Run:
    def __init__(self, ifmaps, weights,  key, B_list, output_file):
       
        index_ = [str(x) for x in B_list]
        columns_ = ["Inputs", "Weights", "Psums"]
        
        meta_is = np.zeros((len(index_), len(columns_)))
        meta_ws = np.zeros((len(index_), len(columns_)))
        meta_os = np.zeros((len(index_), len(columns_)))
        
        for idx, Chnl_blk in enumerate(B_list):
            
        
            
           dram_is = Mem(ifmaps, weights,  Chnl_blk)
           dram_ws = Mem(ifmaps, weights,  Chnl_blk)
           dram_os = Mem(ifmaps, weights,  Chnl_blk)


           
           with open(output_file, "a") as output:
               output.write("Channel Block = " + str(Chnl_blk) + "\n")
               
           IS = Input_Stationary(dram_is, output_file)
           stats[key][Chnl_blk].append(IS.reduction)
           WS = Weight_Stationary(dram_ws, output_file)
           stats[key][Chnl_blk].append(WS.reduction)
           OS = Output_Stationary(dram_os, output_file)
           stats[key][Chnl_blk].append(OS.reduction)
           
#           import pdb; pdb.set_trace()
           
           is_out_buff = np.array(IS.out_buff_val)
           ws_out_buff = np.array(WS.out_buff_val)
           os_out_buff = np.array(OS.out_buff_val)
           
           meta_is[idx][0] = IS.input_transfers 
           meta_is[idx][1] = IS.weight_transfers
           meta_is[idx][2] = IS.psum_transfers
           
           meta_ws[idx][0] = WS.input_transfers 
           meta_ws[idx][1] = WS.weight_transfers
           meta_ws[idx][2] = WS.psum_transfers
           
           meta_os[idx][0] = OS.input_transfers 
           meta_os[idx][1] = OS.weight_transfers
           meta_os[idx][2] = OS.psum_transfers

           if (config.debug):
               res_is = stride_conv(dram_is.inp, dram_is.wt, dram_is.s)
               res_ws = stride_conv(dram_ws.inp, dram_ws.wt, dram_ws.s)
               res_os = stride_conv(dram_os.inp, dram_os.wt, dram_os.s)
                         
               
               
               err_is = is_out_buff - res_is
               err_ws = ws_out_buff - res_ws
               err_os = os_out_buff - res_os
           
               print(err_is)
               print(err_ws)
               print(err_os)
           
           self.ofmaps = stride_conv(dram_is.ifmap, dram_is.wt, dram_is.s)
           
           
        df1 = pd.DataFrame(meta_is, index = index_, columns = columns_) 
        df2 = pd.DataFrame(meta_ws, index = index_, columns = columns_) 
        df3 = pd.DataFrame(meta_os, index = index_, columns = columns_) 
        
        #visualize([df1, df2, df3], ["IS", "WS", "OS"])
	



if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dataset", help ="Name of dataset")
    parser.add_argument("-m", "--model", help ="Name of model") 
    parser.add_argument("-o", "--output", help="Output dump of stats")

    args = parser.parse_args()
    
    

    weight_path_name = '../data/' + args.dataset + '_' + args.model +'_weights'
    images = np.load('../data/' + args.dataset + '_inp.npy')
    images = images[0]
    
    weightdic = []
    stats = {}
    for filename in sorted(os.listdir(weight_path_name)):
        if filename.endswith('.npy'):
            weightdic.append({filename[:-4] : np.load(weight_path_name + '/' + filename)})
            stats.update({filename[:-4]: {}})
            
    
    weightdic.append({"end": -1})
            
    weightdic_iter = iter(weightdic)
    
    curr_layer = list(next(weightdic_iter).keys())[0]
   
    np.save('../results/' + curr_layer + '_inp', images)
    
    B_list = [4, 8, 16]   

        
    for i in weightdic:
        for key,value in i.items():

            output_file = '../results/' + key + '_' + args.output
            stats[key] = {i : [] for i in B_list}
            if not(os.path.isfile(output_file)):
                if (key != 'end'):
                    weights = value
                    inpfile = '../results/' + key + '_inp.npy'
                    if not(os.path.isfile(inpfile)):
                        print("Delete output file of previous layer and start again.")
                        exit() 
                    else:
                        ifmaps = np.load('../results/' + key + '_inp.npy')
                    print('\nBeginning DRAM memory transaction simulation for ' + key)
                    prev = Run(ifmaps, weights, key, B_list, output_file)
                    ifmaps_next = relu(prev.ofmaps)
                    next_layer = list(next(weightdic_iter).keys())[0]
                    np.save('../results/' + next_layer + '_inp', ifmaps_next)
            else:
                dic = collect_stats(B_list, output_file) 
                stats[key].update(dic)
                name = list(next(weightdic_iter).keys())[0]
                if (name != "end"):
                    next_layer = name
                else:
                    print("Simulation finished")
                    f = open("../results/dict.txt", "w")
                    plot(stats,B_list)
                    
                    f.write(str(stats))
                    f.close()
                    
                    exit()
   





   
