#       """""""""""""""""""""""""""""""""""""""""""""""""""""
#              Converting a CSV format to HTML format.
#       """""""""""""""""""""""""""""""""""""""""""""""""""""
import re
import pandas as pd
import glob, os
import argparse
import math

parser = argparse.ArgumentParser(description='Readin a sam file')
parser.add_argument('input')
parser.add_argument('output')
args = parser.parse_args()


f1 = pd.read_csv(args.input,delimiter='\t')
f1.to_html(args.output,index=False)
del f1