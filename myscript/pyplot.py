#       """""""""""""""""""""""""""""""""""""""""""""""""""""
#           Genration of pieplots, barplots, boxplots.
#       """""""""""""""""""""""""""""""""""""""""""""""""""""
import argparse
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns

parser = argparse.ArgumentParser(description='Plots generation')
# pie plot
parser.add_argument('input_pie',help='tsv file for pie plot')
parser.add_argument('output_pie',help='output for pie plot')
# barplot length distribution
parser.add_argument('csv',help='csv file for length distribution')
parser.add_argument('csv_bar',help='output file for length distribution')
# all rRNA class with RPM
parser.add_argument('input_dcsv',help='csv file all rRNA class with RPM')
parser.add_argument('dcsv_box_all',help='output file  all rRNA class with RPM')
# all chr/plt/mt with RPM
parser.add_argument('dcsv_box_chr',help='output file fall chr/plt/mt with RPM')
args = parser.parse_args()


# pie plot
ts_file = pd.read_csv(args.input_pie,delimiter='\t')
rRf = ts_file['rRFs'].to_list()
count = ts_file['counts'].to_list()
colors = ['#B7C3F3', '#DD7596', '#8EB897']
plt.style.use("fivethirtyeight")
plt.pie(count,labels=rRf,wedgeprops={'edgecolor':'white'},shadow=True,
    autopct='%1.1f%%',
    colors=colors)
plt.tight_layout()
plt.savefig(args.output_pie)


# plot 2 barplot length distribution
csv_file = pd.read_csv(args.csv,delimiter='\t')
col2 = csv_file[['Category','Length']].value_counts()
col2_Ex = pd.DataFrame(col2).reset_index()
col2_Ex.columns =['Category','Length','read_count']
g = sns.catplot(
    data=col2_Ex, kind="bar",
    x="Length", y="read_count", hue="Category",
    alpha=1, height=20
)
plt.xlabel('Nucleotide', fontsize=26)
plt.ylabel('RPM', fontsize=26)
g.savefig(args.csv_bar)


# Column Rearrangement  
file2 = pd.read_csv(args.input_dcsv,delimiter='\t')
file2[['rRNA','RNA_type']] = file2['rRNA_info'].str.extract(r'(.*)_rRNA::chr(.*):')
file2['rRNA_class'] = file2['RNA_type'].replace(to_replace='[0-9]',value='Nuc',regex=True)
file2.drop(['RNA_type'],axis=1,inplace=True)
file2['Origin'] = file2['rRNA'].astype(str) + '_' + file2['rRNA_class']

# distribution of all rRNA classes based on RPM and category of rRFs
fig,ax1 = plt.subplots(figsize=(12, 10))
sns.set_theme(style="white", palette="pastel")
sns.boxplot(x="rRNA",y="RPM",hue="Category",
    data=file2)
sns.despine(offset=10, trim=True)
plt.savefig(args.dcsv_box_all)

# distribution of rRFs in nuclear, chloroplast and mitochondrial
fig,ax1 = plt.subplots(figsize=(12, 10))
sns.set_theme(style="white", palette="pastel")
sns.boxplot(x="rRNA_class",y="RPM",hue="Category",
    data=file2)
sns.despine(offset=10, trim=True)
plt.savefig(args.dcsv_box_chr)
