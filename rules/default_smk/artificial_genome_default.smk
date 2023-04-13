# #       """""""""""""""""""""""""""""""""""""""""""""""""""""
# #           Construction of user-defined Artificial Genome
# #       """""""""""""""""""""""""""""""""""""""""""""""""""""

configfile: "config/config.yaml"
rule default_rna_fasta:
    input:
        bed ="data/store/rRNA_AT.bed"
    output:
        "intermediate/Genome/default/{name}/{name}_RNA_gene.fa"
    params:
        fna= config["reference_genome"]["genome_fasta"]
    shell:
        "bedtools getfasta -fi {params.fna} -bed {input.bed} -name -s -fo {output}"

rule default_genome_extract:
    input:
        script = "myscript/build_genome_file.py"
    output:
        "intermediate/Genome/default/{name}/{name}_genome.tmp"
    params:
        fna= config["reference_genome"]["genome_fasta"]
    shell:
        "python3 {input.script} {params.fna} {output}"

rule default_coord_with_flanks:
    input:
        bed = "data/store/rRNA_AT.bed", 
        genome = "intermediate/Genome/default/{name}/{name}_genome.tmp"
    output:
        "intermediate/Genome/default/{name}/{name}_flank.bed"
    params:
        float(config["cord_with_flanks"]["Number"])
    shell:
        "bedtools slop -s -i {input.bed} -g {input.genome} -b {params} > {output}"

rule default_genome_masked:
    input:
        bed = "intermediate/Genome/default/{name}/{name}_flank.bed"
    output:
        "intermediate/Genome/default/{name}/{name}_masked_rna.fa"
    params:
        fna= config["reference_genome"]["genome_fasta"]
    shell:
        "bedtools maskfasta -fi {params.fna} -bed {input.bed} -fo {output} -mc N"

rule default_artificial:
    input: 
        i1 = "intermediate/Genome/default/{name}/{name}_masked_rna.fa",
        i2 = "intermediate/Genome/default/{name}/{name}_RNA_gene.fa"
    output:
        "intermediate/Genome/default/{name}/{name}_genome_artificial.fa"
    shell:
        """
        cat {input.i1} {input.i2} > {output}
        """ 

rule default_indexing:
    input:
        "intermediate/Genome/default/{name}/{name}_genome_artificial.fa"
    output:
        "intermediate/SAM/{name}/{name}_genome_indexed.idx"
    shell: 
        "segemehl.x -x {output} -d {input}"



 
