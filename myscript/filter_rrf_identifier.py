#       """""""""""""""""""""""""""""""""""""""""""""""""""""
# Filtering of rRFs from csv to filtered.csv based on the rRF abundance at a particular genomic location.
#       """""""""""""""""""""""""""""""""""""""""""""""""""""
import re
import pandas as pd
import glob, os
import argparse
import math

parser = argparse.ArgumentParser(description='filtering of the csv file')
parser.add_argument('input',help='raw csv file')  # temporary
parser.add_argument('filter',help='filtered csv for html construction')
parser.add_argument('abundance',help='to get abundance rRFs for each rRNA class')
parser.add_argument('filter_csv',help='uniq mapped read count into csv')  # to be dispalyed
args = parser.parse_args()

# input csv file
table = pd.read_csv(args.input,delimiter='\t')
look = table.value_counts()
look  = pd.DataFrame(look).reset_index()
look.columns = ['Category','rRNA_info','Gene_Start','Gene_End','Sequence','Length','Genomic_Start','Genomic_End','Difference','count','RPM','Seq_count']
look_sort = look.sort_values(by='Seq_count',ascending=False)
lookdrop = look_sort.drop_duplicates(subset=['Genomic_Start','Genomic_End'],keep='first')
# lookup = lookdrop.drop(['Seq_count'],axis=1)

# to find rRFs seq abundance in each rRNA gene
file2 = lookdrop.sort_values(['Seq_count'],ascending=[0])
file_abundant = file2.drop_duplicates(subset=['rRNA_info'],keep='first')
file_abundant = file_abundant.reset_index()
file_abundant.drop(['index','count','Seq_count','RPM'],axis=1,inplace=True)

lookdrop.to_csv(args.filter, index=False, sep='\t')
file_abundant.to_csv(args.abundance, index=False, sep='\t')

#uniq mapped read count
all_Seq = pd.read_csv(args.input,delimiter='\t')
all_Seq = all_Seq[['Category','rRNA_info','Gene_Start','Gene_End','Sequence','Length','Genomic_Start','Genomic_End','Difference','RPM']].value_counts()
tab_seq = pd.DataFrame(all_Seq).reset_index()
tab_seq.columns=['Category','rRNA_info','Gene_Start','Gene_End','Sequence','Length','Genomic_Start','Genomic_End','Difference','RPM','uniq_seq_count']
# tab_seq = tab_seq.sort_values(by=['Genomic_Start','Genomic_End'])
tab_seq.to_csv(args.filter_csv,index=False, sep='\t')

# deleting unnecessary files
del look
del look_sort
del lookdrop
del file_abundant
del file2
del all_Seq
del tab_seq

