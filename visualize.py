#file: visualize.py
#authors: Kamiel Fokkink, Bram Mak

#This code visualizes the results into graphs and tables

import matplotlib.pyplot as plt
import itertools
from math import gcd

def makeBarPlots(counts):
    fig, subfig = plt.subplots(3,2,figsize=(7,8))
    z = zip(counts.items(),itertools.product(range(3),range(2)))
    for (key,value), (i,j) in z:
        if key == None: coninue
        subfig[i,j].bar([k for k in value.keys()],[v/1024 for v in value.values()],0.3,color="b")
        title = "a = " + str(key)
        subfig[i,j].set_title(title)
        subfig[i,j].set_ylim([0,0.55])
    
    for ax in fig.axes:
        plt.sca(ax)
        plt.xticks(rotation=45)    
    plt.delaxes(subfig[2,1])
    plt.subplots_adjust(hspace=1)
    plt.subplots_adjust(wspace=0.3)
    plt.savefig("Results/simulationResults.png")
    #plt.show()    
    
def guessFactors(df,a,N):
    path = "Results/a=" + str(a) + ".csv"
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