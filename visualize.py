#file: visualize.py
#authors: Kamiel Fokkink, Bram Mak

#This code visualizes the results into graphs and tables

import matplotlib.pyplot as plt
import itertools
import numpy as np
from math import gcd
    
def makeBarPlots(counts1,counts2):
    
    counts1,counts2 = processCounts(counts1,counts2)
    
    fig, subfig = plt.subplots(3,2,figsize=(7,8))
    z1 = zip(counts1.items(),itertools.product(range(3),range(2)))
    for (key,value), (i,j) in z1:
        if key == None: coninue
        x = np.arange(len(value))
        subfig[i,j].bar(x-0.2,[v/1024 for v in value.values()],0.3,color="b",label="Simulation")
        title = "a = " + str(key)
        subfig[i,j].set_title(title)
        subfig[i,j].set_ylim([0,0.55])
        subfig[i,j].set_xticks(x)
        subfig[i,j].set_xticklabels([k for k in value.keys()])
    
    z2 = zip(counts2.items(),itertools.product(range(3),range(2)))
    for (key,value), (i,j) in z2:
        if key == None: coninue
        x = np.arange(len(value))
        subfig[i,j].bar(x+0.2,[v/1024 for v in value.values()],0.3,color="r",label="Noise model")
    
    handles, labels = subfig[2,0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center')
    for ax in fig.axes:
        plt.sca(ax)
        plt.xticks(rotation=45)    
    plt.delaxes(subfig[2,1])
    plt.subplots_adjust(hspace=1)
    plt.subplots_adjust(wspace=0.3)
    plt.savefig("Results/simulationResults.png")
    #plt.show()  

def processCounts(c1,c2):
    processedCounts = dict()
    for a,d in c2.items():
        processedCounts[a] = dict()
        for k in d.keys():
            if k in c1[a]:
                processedCounts[a][k] = c1[a][k]
            else:
                processedCounts[a][k] = 0
            if c2[a][k]==1:
                c2[a][k]=2 #Add one for better visualization, as only 1 count is too small to be rendered
    return c1, c2
    
def guessFactors(df,a,N,model):
    path = "Results/" + model + "_a=" + str(a) + ".csv"
    df.to_csv(path,index=False)
    
    r = df.value_counts(subset=["Guess for r"]).index[0][0] #Take most occurring r
    file = open(path,"a")
    line = "Most occurring estimate of r: " + str(r) + "\n"
    file.write(line)
    
    guesses = [gcd(a**(r//2)-1, N), gcd(a**(r//2)+1, N)]
    for guess in guesses:
        if guess not in [1,N] and (N % guess) == 0:
            line = "Found factor: " + str(guess) + "\n"
            file.write(line)