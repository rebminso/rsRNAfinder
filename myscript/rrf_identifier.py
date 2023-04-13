#       """""""""""""""""""""""""""""""""""""""""""""""""""""
#        Identification and Classification of rRFs.
#       """""""""""""""""""""""""""""""""""""""""""""""""""""
import re
import pandas as pd
import glob, os
import argparse
import math
import pandas as pd

parser = argparse.ArgumentParser(description='=============READING A SAM FILE===========')
parser.add_argument('input',help='input sam file name')
parser.add_argument('classify',help='output csv file name')
parser.add_argument('mismatch', help='maximum mismatches in the alignment')
parser.add_argument('rpm', help='RPM threshold')
parser.add_argument('-m','--min',type=int, help='minimun Length of rRFs')
parser.add_argument('-M','--max',type=int, help='maximum Length of rRFs')
args = parser.parse_args()



with open(args.input, 'r') as sam1:
    sam = sam1.readlines()
    semi_Tab_list= []
    for line in sam:
        if not line.startswith('@'):
            line3 = line.split('\t')
            # # line3 = line2.split()
            semi_tab =  line3[0] + '\t' + line3[2] + '\t' + line3[3] +'\t'+  str(len(line3[9])) + '\t' + line3[9] + '\t'+ line3[11]
            semi_Tab_list.append(semi_tab)
semi_tab = pd.DataFrame(semi_Tab_list,columns=['title'])
del sam
del sam1
del semi_Tab_list
semi_tab[['Sampleid','rRNA_info','Gene_Start','Length','Sequence','info']] = semi_tab['title'].str.extract(r'(.*)\t(.*)\t(.*)\t(.*)\t(.*)\t(.*)')
semi_tab = semi_tab.drop(['title'],axis=1)

#per-million factor
Total_Sample = len(pd.unique(semi_tab['Sampleid']))
Per_million_factor = (Total_Sample)/(10**6)
semi_tab = semi_tab.loc[(semi_tab['rRNA_info'].str.contains('rRNA',regex=True))].reset_index(drop=True)
semi_tab[['genomicS','genomicE','strand']]=semi_tab['rRNA_info'].str.extract(':([0-9].*)-([0-9].*)\((.*)\)')
semi_tab=semi_tab.fillna(0)
semi_tab = semi_tab.astype({'genomicS':'int','Gene_Start':'int','genomicE':'int','Length':'int'})
semi_tab['Genomic_Start'] = semi_tab['genomicS'] + semi_tab['Gene_Start']
semi_tab['Genomic_End'] = semi_tab['Genomic_Start'] + semi_tab['Length'] -1
semi_tab['Gene_End'] = semi_tab['Gene_Start'] + semi_tab['Length']
semi_tab = semi_tab.astype({'Genomic_Start':'int','Genomic_End':'int','genomicE':'int'})

tab = semi_tab[['Genomic_Start','Genomic_End']].value_counts()
tab = pd.DataFrame(tab).reset_index()
tab.columns = ['Genomic_Start','Genomic_End','Count']
merged_table = pd.merge(semi_tab,tab,on=['Genomic_Start','Genomic_End'])
del tab
del semi_tab
merged_table['Difference'] = merged_table['info'].str.extract(r'NM:i:(.*)')
merged_table = merged_table.drop(['info'],axis=1)
merged_table = merged_table.astype({'Difference':'int'})
values_sorted = merged_table.loc[(merged_table['Difference']<int(args.mismatch))]
del merged_table


# classification
first = 1
values_sorted.loc[(values_sorted['Genomic_Start'] <= (values_sorted['genomicS']+first)),'Category'] = 'rRF-5'
values_sorted.loc[(values_sorted['Genomic_End'] >= (values_sorted['genomicE']-first)),'Category'] = 'rRF-3'
values_sortedle = values_sorted.fillna('rRF-i')
values_sortedle['RPM'] = values_sortedle['Count']/Per_million_factor
del values_sorted
values_sortedle = values_sortedle[['Category','rRNA_info','Gene_Start','Gene_End','Sequence','Length','Genomic_Start','Genomic_End','Difference','Count','RPM']]
values_sortedle2 = values_sortedle.loc[(values_sortedle['Length'] >= args.min) & (values_sortedle['Length'] <= args.max)]
values_sortedle2 = values_sortedle2.loc[(values_sortedle2['RPM']>int(args.rpm))]



values_sortedle2.to_csv(args.classify, index=False, sep='\t')
del values_sortedle
del values_sortedle2

