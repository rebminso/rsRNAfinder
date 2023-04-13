#       """""""""""""""""""""""""""""""""""""""""""""""""""""
#                    Extracting chromosome lengths.
#       """""""""""""""""""""""""""""""""""""""""""""""""""""
from Bio import SeqIO
import sys
import argparse


parser = argparse.ArgumentParser(description='extract genome file')
parser.add_argument('input')
parser.add_argument('output')
args = parser.parse_args()

#Extract chromosome lengths
print("USAGE: python3 build_genome_file.python <FASTA FILE>")
print("Extracting chromosome lengths from %s ..." % str(sys.argv[1]))

ids = []
lengths = []
for rec in SeqIO.parse(args.input, "fasta"):
        ids.append(rec.id)
        lengths.append(len(rec))

#Write genome file - tab delimited text file
with open(args.output, "w") as outf:
        for id, length in zip(ids, lengths):
                chrom_record = [str(id), str(length)]
                outf.write("\t".join(chrom_record) + "\n")

outf.close()
print("Chromosome lengths extracted.")
