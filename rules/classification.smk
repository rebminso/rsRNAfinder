#       """""""""""""""""""""""""""""""""""""""""""""""""""""
#             Identification and classification of rRFs
#       """""""""""""""""""""""""""""""""""""""""""""""""""""

configfile: "config/config.yaml"

rule classification:
    input:
        i1 = "intermediate/SAM/{name}/{dir}/{sample}/{sample}_trimmed.sam",
        script="myscript/rrf_identifier.py"
    output:
        o1 = temp("results/{name}/{dir}/{samplew}/{sample}.csv"),
    threads:
        8
    params:
        min=config['Define_rRFs_length']['min_length'],
        max=config['Define_rRFs_length']['max_length'],
        diff=config['mismatches']['max'],
        rpm=config['rpm']['threshold']
    shell:
        "python {input.script} {input.i1} -m {params.min} -M {params.max} {output.o1} {params.diff} {params.rpm}"

rule filtering_csv:
    input:
        i1 = "results/{name}/{dir}/{sample}/{sample}.csv",
        script="myscript/filter_rrf_identifier.py"
    output:
        o1 = temp("results/{name}/{dir}/{sample}/{sample}_filtered.csv"), # to be used for constructing html file
        o2 = "results/{name}/{dir}/{sample}/{sample}_abundant_rRFs_summary.csv",
        o3 = "results/{name}/{dir}/{sample}/{sample}_Filtered.csv" # to be visible
    threads:
        8
    shell:
        "python {input.script} {input.i1} {output.o1} {output.o2} {output.o3}"

rule tsv:
    input:
        i1="results/{name}/{dir}/{sample}/{sample}_filtered.csv",
        script="myscript/rRNA_stat.py"
    output:
        "results/{name}/{dir}/{sample}/{sample}_filtered.tsv"
    shell:
        "python {input.script} {input.i1} {output}"


rule piplot:
    input:
        i1 = "results/{name}/{dir}/{sample}/{sample}_filtered.tsv",
        script = "myscript/pyplot.py",
        bar = "results/{name}/{dir}/{sample}/{sample}_filtered.csv",
        bar2 = "results/{name}/{dir}/{sample}/{sample}_filtered.csv"
    output:
        pie = "results/{name}/{dir}/{sample}/{sample}_filtered_piplot.png",
        bar = "results/{name}/{dir}/{sample}/{sample}_filtered_length_distribution.png",
        box_All = "results/{name}/{dir}/{sample}/{sample}_filtered_boxplot_All.png",
        box_chr = "results/{name}/{dir}/{sample}/{sample}_filtered_box_chr.png"

    shell:
        """
        python {input.script} {input.i1} {output.pie} {input.bar} {output.bar} {input.bar2} {output.box_All} {output.box_chr}
        """

rule vienna:
    input:
        i1="results/{name}/{dir}/{sample}/{sample}_filtered.csv",
        i2="myscript/rnafold.py"
    output:
       temp("results/{name}/{dir}/{sample}/{sample}_seq_list.txt")
    shell:
        """
        python {input.i2} {input.i1} {output}
        """

rule get_notation:
    input:
        "results/{name}/{dir}/{sample}/{sample}_seq_list.txt"
    output:
        temp("results/{name}/{dir}/{sample}/{sample}_rnafold.txt")
    shell:
        "RNAfold {input[0]} > {output[0]} && find . -name '*.ps'|xargs rm"

rule final_table:
    input:
        i1="results/{name}/{dir}/{sample}/{sample}_rnafold.txt",
        i2="results/{name}/{dir}/{sample}/{sample}_filtered.csv",
        myscript ="myscript/rnafold2.py"
    output:
        temp("results/{name}/{dir}/{sample}/{sample}_filtered_TABLE.csv")
    shell:
        """
        python {input.myscript} {input.i2} {input.i1} {output} 
        """

rule html:
    input:
        i1="results/{name}/{dir}/{sample}/{sample}_filtered_TABLE.csv",
        script="myscript/csv_to_html.py"
    output:
        "results/{name}/{dir}/{sample}/{sample}_filtered.html"
    shell:
        "python {input.script} {input.i1} {output}"
