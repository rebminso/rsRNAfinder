#       """""""""""""""""""""""""""""""""""""""""""""""""""""
#                Construction of Artificial Genome
#       """""""""""""""""""""""""""""""""""""""""""""""""""""

configfile: "config/config.yaml"
rule rRNA_genes_extraction:
    input:
        config['reference_genome']['species_NCBI_feature_table']
    output:
        "intermediate/Genome/User_defined/{name}/{name}.bed"
    shell:
        """
        cat {input} |
        grep 'S ribosomal RNA' |
        cut -f6,8,9,10,14 |
        sed 's/^/chr/g; s/ //g; s/ribosomalRNA/_rRNA/g' |
        grep -v -w 'chr' > {output}
        """ 

rule dot_column:
    input:
        "intermediate/Genome/User_defined/{name}/{name}.bed"
    output:
        "intermediate/Genome/User_defined/{name}/{name}_2.bed"
    shell:
        """
        awk \'BEGIN{{ FS=OFS="\\t" }} {{$4 = $4 FS (NR==1? "." : ".") }}1\' {input} > {output}
        """

rule rearrange:
    input:
        "intermediate/Genome/User_defined/{name}/{name}_2.bed"
    output:  
        "intermediate/Genome/User_defined/{name}/{name}_3.bed"
    shell:
        "paste <(cut -f1,2,3,6 {input}) <(cut -f5 {input}) <(cut -f4 {input})> {output};"

rule genome_extract:
    input:
        script = "myscript/build_genome_file.py"
    output:
        "intermediate/User_defined/{name}/Genome_genome.tmp"
    params:
        fna= config["reference_genome"]["genome_fasta"]
    shell:
        "python3 {input.script} {params.fna} {output}"

rule coord_with_flanks:
    input:
        bed = "intermediate/Genome/User_defined/{name}/{name}_3.bed",
        genome = "intermediate/User_defined/{name}/Genome_genome.tmp"
    output:
        "intermediate/Genome/User_defined/{name}/{name}_flank.bed"
    params:
        float(config["cord_with_flanks"]["Number"])
    shell:
        "bedtools slop -s -i {input.bed} -g {input.genome} -b {params} > {output}"

rule coord_with_sorted_flanks:
    input:
        "intermediate/Genome/User_defined/{name}/{name}_flank.bed"
    output:
        "intermediate/Genome/User_defined/{name}/{name}_flank_sorted.bed"
    shell:
        "bedtools sort -i {input} > {output}"

rule flank_fasta:
    input:
        bed = "intermediate/Genome/User_defined/{name}/{name}_flank_sorted.bed"
    output:
        "intermediate/Genome/User_defined/{name}/{name}_flank.fasta"
    params:
        fna= config["reference_genome"]["genome_fasta"]
    shell:
        "bedtools getfasta -name -s -fi {params.fna} -bed {input.bed} -fo {output}"

rule masking_genome:
    input:
        bed = "intermediate/Genome/User_defined/{name}/{name}_flank_sorted.bed"
    output:
        "intermediate/Genome/User_defined/{name}/{name}_masked_genome.fa"
    params:
        fna= config["reference_genome"]["genome_fasta"]
    shell:
        "bedtools maskfasta -fi {params.fna} -bed {input.bed} -fo {output} "

rule artificial_genome:
    input:
        genomefa = "intermediate/Genome/User_defined/{name}/{name}_masked_genome.fa",
        flankfa = "intermediate/Genome/User_defined/{name}/{name}_flank.fasta"
    output:
        "intermediate/Genome/User_defined/{name}/{name}_genome_artificial.fa"
    shell:
        "cat {input.genomefa} {input.flankfa} > {output}"

rule index_NCBI_genome:
    input:
        "intermediate/Genome/User_defined/{name}/{name}_genome_artificial.fa"
    output:
        "intermediate/SAM/{name}/{name}_genome_indexed.idx"
    shell: 
        "segemehl.x -x {output} -d {input}"
