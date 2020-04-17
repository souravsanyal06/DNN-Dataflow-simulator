import pandas as pd
import matplotlib.cm as cm
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def visualize(dfall, labels=None, title="DRAM Transactions",  H="/", **kwargs):
    """Given a list of dataframes, with identical columns and index, create a clustered stacked bar plot. 
labels is a list of the names of the dataframe, used for the legend
title is a string for the title of the plot
H is the hatch used for identification of the different dataframe"""

    n_df = len(dfall)
    n_col = len(dfall[0].columns) 
    n_ind = len(dfall[0].index)
    axe = plt.subplot(111)

    for df in dfall : # for each data frame
        axe = df.plot(kind="bar",
                      linewidth=0,
                      stacked=True,
                      ax=axe,
                      legend=False,
                      grid=False,
                      **kwargs)  # make bar plots

    h,l = axe.get_legend_handles_labels() # get the handles we want to modify
    for i in range(0, n_df * n_col, n_col): # len(h) = n_col * n_df
        for j, pa in enumerate(h[i:i+n_col]):
            for rect in pa.patches: # for each index
                rect.set_x(rect.get_x() + 1 / float(n_df + 1) * i / float(n_col))
                rect.set_hatch(H * int(i / n_col)) #edited part     
                rect.set_width(1 / float(n_df + 1))

    axe.set_xticks((np.arange(0, 2 * n_ind, 2) + 1 / float(n_df + 1)) / 2.)
    axe.set_xticklabels(df.index, rotation = 0)
    axe.set_title(title)

    # Add invisible data to add another legend
    n=[]        
    for i in range(n_df):
        n.append(axe.bar(0, 0, color="gray", hatch=H * i))

    l1 = axe.legend(h[:n_col], l[:n_col], loc=[1.01, 0.5])
    if labels is not None:
        l2 = plt.legend(n, labels, loc=[1.01, 0.1]) 
    axe.add_artist(l1)
    plt.show()
    #plt.draw()
    plt.yscale('log')
    
    return axe

def plot(dic, blist):
    index = list(dic.keys())
    
    for i in blist:
        IS = []
        WS = []
        OS = []
        for j in range(len(index)):
            IS.append(dic[index[j]][i][0])
            WS.append(dic[index[j]][i][1])
            OS.append(dic[index[j]][i][2])
        w = 0.25    
        r1 = np.arange(len(IS))
        r2 = [x + w for x in r1]
        r3 = [x + w for x in r2]
        
        plt.bar(r1, IS, width = w, label = 'IS')
        plt.bar(r2, WS, width = w, label = 'WS')
        plt.bar(r3, OS, width = w, label = 'OS')
        
        plt.xticks([r + w for r in range(len(index))], index)
        plt.xticks(rotation = 90)
        plt.legend()
        plt.ylabel('% Reduction', size = 15)
        plt.tight_layout()
        plt.show()
    
    
        
        
        
            
        
    
    
