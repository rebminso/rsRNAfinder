# ############################################################################################################################
#         To generate an input file for RNAFold
# ############################################################################################################################

import re
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='a list of seq from csv file')
parser.add_argument('input',help='final csv file')
parser.add_argument('seq_output',help='sequence output')
args = parser.parse_args()



import pandas as pd
all_Seq = pd.read_csv(args.input,delimiter='\t')
Sequence_list = []
seq = all_Seq['Sequence'].to_list()
for i in range(len(seq)):
    abc = '>{}\n{}'.format(i,seq[i])
    Sequence_list.append(abc)
# print(Sequence_list)
with open(args.seq_output,'w') as a1:
    for items in Sequence_list:
        a1.write(items+"\n")
a1.close()

