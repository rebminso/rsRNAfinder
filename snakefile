configfile: "config/config.yaml"

import glob,os
import pandas

# fetching directory and sample names
directories, Samples =glob_wildcards("data/trimmed/{dir}/{file}_trimmed.fq")

# fetching reference genome name
id2 = config['reference_genome']["genome_fasta"]
a2 = glob.glob(id2)
Names = []
for i2 in range(0,len(a2)):
    ids2 = os.path.basename(a2[i2])
    ids2 = ids2.replace('.fna','')
    Names.append(ids2)

count = 0
for i in Samples:
    count = count +1
NAME = Names*count

rule all:
    input:
        expand("results/{name}/{dir}/{sample}/{sample}_Filtered.csv",zip,sample=Samples,dir=directories,name=NAME),
        expand("results/{name}/{dir}/{sample}/{sample}_filtered_piplot.png",zip,sample=Samples,dir=directories,name=NAME),
        expand("results/{name}/{dir}/{sample}/{sample}_filtered_length_distribution.png",zip,sample=Samples,dir=directories,name=NAME),
        expand("results/{name}/{dir}/{sample}/{sample}_filtered.html",zip,sample=Samples,dir=directories,name=NAME),
        expand("results/{name}/{dir}/{sample}/{sample}_filtered_boxplot_All.png",zip,sample=Samples,dir=directories,name=NAME),
        expand("results/{name}/{dir}/{sample}/{sample}_abundant_rRFs_summary.csv",zip,sample=Samples,dir=directories,name=NAME),
        expand("results/{name}/{dir}/{sample}/{sample}_filtered_box_chr.png",zip,sample=Samples,dir=directories,name=NAME),
        expand("results/{name}/{dir}/{sample}/{sample}_seq_list.txt",zip,sample=Samples,dir=directories,name=NAME),
	
 

strategy = config['reference_genome']['Search_strategy']
print("Search_strategy: ",strategy)
if strategy == "Default":
    include: "rules/default_smk/artificial_genome_default.smk"
    include: "rules/default_smk/alignment_default.smk"
    include: "rules/classification.smk"

else:
    include: "rules/User_defined/artificial_genome.smk"
    include: "rules/User_defined/alignment.smk"
    include: "rules/classification.smk"

