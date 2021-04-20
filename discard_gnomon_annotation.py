#!/usr/bin/python
# modifies *.gff3 annotation file by dropping off "Curated Genomic" pseudogenes and Gnomon records. gff file has to have its header.

import sys
import pandas as pd

infile = sys.argv[1]
outfile = sys.argv[2]

df = pd.read_csv(infile, sep="\t", header=None)
df = df.loc[df[1] != 'Gnomon']
df = df.loc[df[1] != 'Curated Genomic']
df = df.loc[df[1] != 'cmsearch']

print('Writing file: {}'.format(outfile))
df.to_csv(outfile, sep="\t", header=False, index=False)

