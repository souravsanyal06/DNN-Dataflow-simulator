import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

debug = 1

PE_height = 8
PE_width = 8


KB = 1024

# for each PE 

input_buffer = 0.5 * KB
weight_buffer = 0.5 * KB
psum_buffer = 0.5 * KB

#considering 16 bit or 2 byte fixed point representation

sram_inp = int(input_buffer/2)
sram_wt = int(weight_buffer/2)
sram_psum = int(psum_buffer/2)
