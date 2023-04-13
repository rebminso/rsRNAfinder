#       """""""""""""""""""""""""""""""""""""""""""""""""""""
#          Extraction of rRFs with RPM configured threshold.
#       """""""""""""""""""""""""""""""""""""""""""""""""""""
import re
import pandas as pd
import glob, os
import argparse
import math


parser = argparse.ArgumentParser(description='filtering_sam_csv')
parser.add_argument('input_threshold')
parser.add_argument('input_csv')
parser.add_argument('output')
args= parser.parse_args()

with open(args.input_threshold,'r') as f1:
    f1 = f1.readline()
    f2 = f1.split()
    f3 = f2[3]
    print(f3)
        # w1.write(f3)

sam = pd.read_csv(args.input_csv,delimiter='\t')
# print(sam.head(4))
sam_filt = sam.loc[(sam['RPM']>=int(f3))]
# sam_filt = sam_filt.sort_values(by=['Sampleid'])
sam_filt.to_csv(args.output,index=False,sep='\t')

