#!/usr/bin/python
import sys
import pandas as pd


# define chromosomes to keep
mm_chroms = ['NC_000067.6',
                  'NC_000068.7',
                  'NC_000069.6',
                  'NC_000070.6',
                  'NC_000071.6',
                  'NC_000072.6',
                  'NC_000073.6',
                  'NC_000074.6',
                  'NC_000075.6',
                  'NC_000076.6',
                  'NC_000077.6',
                  'NC_000078.6',
                  'NC_000079.6',
                  'NC_000080.6',
                  'NC_000081.6',
                  'NC_000082.6',
                  'NC_000083.6',
                  'NC_000084.6',
                  'NC_000085.6',
                  'NC_000086.7',
                  'NC_000087.7']

# get these ones with this: cat GRCh38.p13.genome.fa | grep ">" | less
hg_chroms = ['NC_000010.11',
'NC_000011.10',
'NC_000012.12',
'NC_000013.11',
'NC_000014.9',
'NC_000015.10',
'NC_000016.10',
'NC_000017.11',
'NC_000018.10',
'NC_000019.10',
'NC_000001.11',
'NC_000020.11',
'NC_000021.9',
'NC_000022.11',
'NC_000002.12',
'NC_000003.12',
'NC_000004.12',
'NC_000005.10',
'NC_000006.12',
'NC_000007.14',
'NC_000008.11',
'NC_000009.12']

# genome version
chromosomes = mm_chroms
if len(sys.argv) >= 4:
    genome = sys.argv[3] # can be: hg/human/hg38/hg19 or mm/mm10/mouse
    if genome in ['hg', 'hg38', 'hg19', 'human']:
         chromosomes = hg_chroms

infile = sys.argv[1]
outfile = sys.argv[2]

df = pd.read_csv(infile, sep="\t", header=None, comment='#')
df = df.loc[df[0].isin(chromosomes)]
df.to_csv(outfile, sep="\t", header=False, index=False)

