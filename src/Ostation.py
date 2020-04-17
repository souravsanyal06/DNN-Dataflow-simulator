import numpy as np
import sys
import os
import math
import collections as cl

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Mem import *
import config

class Output_Stationary:
    def __init__(self,m, fout):
       
        print('\n......Output Stationary.....\n')
        A = int(math.ceil(m.Cout/m.Co_b))
        A = 1 if A == 0 else A
        
        self.input_transfers = 0
        self.weight_transfers = 0
        self.input_transfers_sparse = 0
        self.weight_transfers_sparse = 0
        self.psum_transfers = 0

        beg = 0
        end = m.Co_b
        
        final = np.zeros((m.Cout, m.Wo_t, m.Ho_t))
        
        isram = cl.deque(maxlen = config.sram_inp)
        wsram = cl.deque(maxlen = config.sram_wt)
        osram = cl.deque(maxlen = config.sram_psum)
        
        wsram_sparse = cl.deque(maxlen = config.sram_wt)
                
        for k_b in range (A):
            wt_b = m.wt[:,beg:end]
            
            out_act = np.zeros(( m.Co_b, m.Wo_t, m.Ho_t))
            inp = np.array([ [ [o.value for o in i] for i in j ] for j in m.inp])
            wt = np.array([ [  [ [o.value for o in i] for i in j] for j in k] for k in wt_b])
            
            for c in range (m.Cin):    
                for ii in range (0, inp[c].shape[0]-2,m.s):
                    for jj in range (0, inp[c].shape[0]-2,m.s):
                       for i in m.wt[c,beg:end]:
                           for j in i:
                               for k in j:
                                   if (k.value in wsram):
                                       if (k.value is wsram[wsram.index(k.value)]):
                                           pass
                                       else:
                                           k.increment_densecount()
                                           wsram.append(k.value)
                                   else:
                                       k.increment_densecount()
                                       wsram.append(k.value)
                                  # import pdb; pdb.set_trace()
                                   if (inp[c][ii][jj] != 0):
                                       if (k.value in wsram_sparse):
                                           if (k.value is wsram_sparse[wsram_sparse.index(k.value)]):
                                               pass
                                           else:
                                               k.increment_sparsecount()
                                               wsram_sparse.append(k.value)
                                       else:
                                           k.increment_sparsecount()
                                           wsram_sparse.append(k.value)
                           wsram.clear()
                           wsram_sparse.clear()
                for jj in range (0, 2*inp[c].shape[0]-2,m.s):
                    for i in  m.inp[c]:
                        for j in i:
                            if (j.value in isram):
                                if (j.value is isram[isram.index(j.value)]):
                                    pass
                                else:
                                    j.increment_densecount()
                                    j.increment_sparsecount()
                                    isram.append(j.value)
                            else:
                                j.increment_densecount()
                                j.increment_sparsecount()
                                isram.append(j.value)
                    isram.clear()    
                        

            
            for op_ch in range (m.Co_b): #Output channels
                
                            
                beg_ = 0
                end_ = wt[0][op_ch].shape[0]
                out = [ [] for c in range(m.Cin)]
                for i in range(0,inp[0].shape[0]-2,m.s): #Input Width
                    k = [ [] for c in range(m.Cin)]
                    for j in range(0,inp[0].shape[0]-2,m.s): #Input Height
                        for c in range(m.Cin):  #Input Channels
                            
                            i_mat = inp[c][beg_+i:end_+i, beg_+j:end_+j]
                            w_mat = wt[c][op_ch]
                            psum = 0
                            
                            for i_ in range(end_):
                               for j_ in range(end_):
                                   psum += i_mat[i_,j_]*w_mat[i_,j_]
                                   
                            k[c].append(psum)
                            #self.psum_transfers += 1
                            #k.append(np.sum(inp[c][beg_+i : end_+i, beg_+j:end_+j] * (wt[c][op_ch])))
                    for i in range(len(k)):
                        out[i].append(k[i])
                        if (psum in osram):
                            if (psum is osram[osram.index(psum)]):
                                pass
                            else:
                                self.psum_transfers += 1
                                osram.append(psum)
                        else:
                            self.psum_transfers += 1
                            osram.append(psum)
                out = np.array(out)
                osram.clear()
                                    
                for i in range(out.shape[0]):
                    out_act[op_ch] += out[i]
                    

            final[beg:end] = out_act 
                            
            beg = end
            end += m.Co_b 
            
        self.out_buff_val = final
        
        

        for i in m.inp:
            for j in i:
                for k in j:
                    self.input_transfers += k.dense_count
                    self.input_transfers_sparse += k.sparse_count
        
        for i in m.wt:
            for j in i:
                for k in j:
                    for l in k:
                        self.weight_transfers += l.dense_count
                        self.weight_transfers_sparse += l.sparse_count
                
        self.total = self.input_transfers + self.weight_transfers + self.psum_transfers 
        self.total_sparse = self.input_transfers_sparse + self.weight_transfers_sparse + self.psum_transfers
        self.reduction = (float(self.total - self.total_sparse)/float(self.total))*100

        with open(fout, "a") as output:
            output.write("Output Stationary Dense\t")
            output.write(str(int(self.input_transfers)) + "\t")
            output.write(str(int(self.weight_transfers)) + "\t")
            output.write(str(int(self.psum_transfers)) + "\t")
            output.write(str(int(self.total)) + "\n")
            output.write("Output Stationary Sparse\t")
            output.write(str(int(self.input_transfers_sparse)) + "\t")
            output.write(str(int(self.weight_transfers_sparse)) + "\t")
            output.write(str(int(self.psum_transfers)) + "\t")
            output.write(str(int(self.total_sparse)) + "\n")
            output.write("Output Stationary Reduction\t")
            output.write(str(int(self.reduction)) + "\n")

     




