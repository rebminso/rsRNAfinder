#       """""""""""""""""""""""""""""""""""""""""""""""""""""
#          Count distribution of all the three rRFs.
#       """""""""""""""""""""""""""""""""""""""""""""""""""""

import re
import pandas as pd
import glob, os
import argparse
import math

parser = argparse.ArgumentParser(description='Readin a sam file')
parser.add_argument('input')
parser.add_argument('statistics')
args = parser.parse_args()


table = pd.read_csv(args.input,delimiter='\t')
tb = table['Category'].value_counts().rename_axis('rRFs').reset_index(name='counts')
tb.to_csv(args.statistics, index=False, sep='\t')

