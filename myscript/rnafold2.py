#############################################################################################################################
#         To concatenate Dot-bracket notation
#############################################################################################################################

import re
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='a list of seq from csv file')
parser.add_argument('input',help='csv file')
parser.add_argument('rnafold',help='rnafold_output')
parser.add_argument('final_table',help='final table')
args = parser.parse_args()


# rnafold output
fold = pd.read_csv(args.rnafold,names=['Dot-bracket notation (MFE)'])
F = fold.loc[(fold['Dot-bracket notation (MFE)'].str.contains('.\(|.\)',regex=True))].reset_index()
F1 = F.drop('index',axis=1)

# csv file
all_Seq = pd.read_csv(args.input,delimiter='\t')

final_TABLE = pd.concat([all_Seq,F1],axis=1)
final_TABLE.to_csv(args.final_table,index=False, sep='\t')
