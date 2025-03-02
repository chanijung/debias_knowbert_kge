# -*- coding: utf-8 -*-
"""
Modified by chanijung

Original file Exposing_Bias_BERT.ipynb is written by keitakurita,
which is located at https://colab.research.google.com/drive/1vXKmNVVn6se0zjqu2D_Y6_rdX0GpZ3kq
"""

# Commented out IPython magic to ensure Python compatibility.
import torch
import pandas as pd
import numpy as np
from pathlib import Path
from typing import *
import matplotlib.pyplot as plt
import sys
sys.path.append("../lib")

from bert_expose_bias_with_prior import *

from tqdm import tqdm
import time
import os



def Txt2List(file):
    ll=[]
    with open(file) as f:
        for line in f:
            ll.append(line.strip().lower().replace("_", " "))
    return ll

def plot_pie(file, mc=50, fc=50):
    # Data to plot
    labels = 'Male', 'Female'
    sizes = [mc, fc]
    colors = ['lightcoral', 'lightskyblue']

    # Plot
    fig = plt.figure()
    plt.pie(sizes, labels=labels, colors=colors,
    autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')

    tmp = file.split('/')[-1]
    fig.savefig(tmp)

    fig.savefig(file)

    plt.show()
    
def list2Bias_norm(output_dir, plotfile, var_list, abs_str, print_str): #Example of abs_str is "good at ", print_str is "is good at "
    mc=0
    fc=0
    for var in tqdm(var_list):
        strr = abs_str+ var
        ans = bias_score("GGG is XXX", ["he", "she"], strr)
        score= ans['gender_fill_bias_prior_corrected']

        if score>=0:
            mc+=1
            print("Man ",print_str,  var, " by ", score)

        else:
            fc+=1
            print("Woman ",print_str,  var, " by ", score)

    plot_pie(os.path.join(output_dir, plotfile), mc, fc)
    
    
def list2Bias(output_dir, plotfile, var_list, abs_str): #Example of abs_str "is good at "
    start = time.time()
    mc=0
    fc=0
    for var in tqdm(var_list):
        
        score = get_log_odds("[MASK] %s%s"%(abs_str,var), "he", "she")
        
        if score>=0:
            mc+=1
            # print("Man ",abs_str,  var, " by ", score)

        else:
            fc+=1
            # print("Woman ",abs_str,  var, " by ", score)
        
    print(f'mc {mc}, fc {fc}')
    plot_pie(os.path.join(output_dir, plotfile), mc, fc)
    print(f'{(time.time()-start)/60} min spent')




"""# Exposing Bias in BERT


In this notebook, I'll experiment with a couple of possibilities for exposing Bias in BERT. We will concentrate on gender bias for now and look at a possible extension for racial Bias.
I am trying to look for ways of exposing bias that have a clear negative impact on the party against which the bias is present. But for each of these, we will need a good dataset (so, we might want to replace current datasets with larger/reliable/authoritative datasets in the future)
Currently, I am using the Masked Prediction Task but we might be able to extend this for Next Sentence Prediction as well.
We will classify the types of negative impact that are possible and look at experiments on their possible causes-



## 1) Economic/Professional Impact-

Employers may use searching/ranking based on certain skills or job titles . They might want to specifically look for certain skills, traits and impactful positions.

"""
### b) Bias for associating positive traits with a group - 


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--output_dir', type=str)
    args = parser.parse_args()


    #Load Dataset
    print(f'--------positive traits---------')
    pos_traits_list = Txt2List('bin/debiasing_words/refined_positive_traits')

    list2Bias(args.output_dir,'positive_traits.pdf', pos_traits_list, "is ")
    list2Bias_norm(args.output_dir, 'positive_traits_without_prior.pdf', pos_traits_list, " ", "is ")

    ### c) Bias for associating negative traits with a  group - """

    #Load Dataset
    print(f'--------negative traits---------')
    neg_traits_list = Txt2List('bin/debiasing_words/refined_negative_traits')

    list2Bias(args.output_dir, 'negative_traits.pdf', neg_traits_list, "is ")
    list2Bias_norm(args.output_dir, 'negative_traits_without_prior.pdf', neg_traits_list, " ", "is ")

    ### d) Bias for associating high salary jobs with a group - 

    print(f'--------top job titles---------')
    Top_Titles = Txt2List('bin/debiasing_words/refined_job_titles.txt')
    # print(f'top titles len {len(Top_Titles)}')

    list2Bias(args.output_dir, 'highpaying_jobs.pdf', Top_Titles, "is ")
    list2Bias_norm(args.output_dir, 'TopTitles_without_prior.pdf', Top_Titles, " ", "is ")

