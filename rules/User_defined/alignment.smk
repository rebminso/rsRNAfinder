#       """""""""""""""""""""""""""""""""""""""""""""""""""""
#     Alignment of fastq file to indexed genome using segmehel.
#       """""""""""""""""""""""""""""""""""""""""""""""""""""
rule align_to_genome:
    input:
        "intermediate/Genome/User_defined/{name}/{name}_genome_artificial.fa",
        "data/trimmed/{dir}/{sample}_trimmed.fq",
        "intermediate/SAM/{name}/{name}_genome_indexed.idx"
    output:
        temp("intermediate/SAM/{name}/{dir}/{sample}/{sample}_trimmed.sam")

    shell:
        """
        time segemehl.x -t 16 -D 2 -M 50 -x {input[2]} -d {input[0]} -q {input[1]} > {output}
        """
