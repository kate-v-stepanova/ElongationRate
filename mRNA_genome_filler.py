#!/usr/bin/python

# fills 5'UTRs and 3'UTRs shorter than 100 with nucleotides inferred from .gff annotation and genome sequence.
# temp3 file is taken as a result of mRNA_extractor.pl

def reverse_complement(seq):
    res = ''
    for i in range(len(seq)-1, -1, -1):
        if seq[i].upper() == 'A':
            res += 'T'
        elif seq[i].upper() == 'T':
            res += 'A'
        elif seq[i].upper() == 'C':
            res += 'G'
        elif seq[i].upper() == 'G':
            res += 'C'
        else:
            print('Unexpected character: ' + seq[i])
            import pdb; pdb.set_trace()
            res += 'N'
    return res
         

import sys
import os
import pandas as pd

infile = sys.argv[1] # this one: /icgc/dkfzlsdf/analysis/OE0532/static/elongation/temp3
genome = sys.argv[2] # should be 1-line fasta: /icgc/dkfzlsdf/analysis/OE0532/static/elongation/hg38/GRCh38.p13.genome_1line.fa
annotation = sys.argv[3]
outfile = '/icgc/dkfzlsdf/analysis/OE0532/static/elongation/hg38/mRNA_100.fasta'
if len(sys.argv) >= 5:
    outfile = sys.argv[4]

skip1 = False
if os.path.isfile("/icgc/dkfzlsdf/analysis/OE0532/static/elongation/hg38/mRNA.step1.tsv"):
    infile = "/icgc/dkfzlsdf/analysis/OE0532/static/elongation/hg38/mRNA.step1.tsv"
    skip1 = True


df = pd.read_csv(infile, sep="\t")
g_df = pd.read_csv(genome, sep="\n", header=None)
a_df = pd.read_csv(annotation, sep="\t", header=None)

chrs = g_df.loc[g_df[0].str.startswith('>')][0].tolist()
seqs = g_df.loc[~g_df[0].str.startswith('>')][0].tolist()

chroms = pd.DataFrame(columns=['chr', 'seq'])
chroms['chr'] = chrs
chroms['seq'] = seqs

# iff not 1 line:
#chroms = g_df.loc[g_df[0].str.startswith('>')]
#chroms['start'] = chroms.index + 1
#chroms['end'] = chroms['start'].tolist()[1:] + [len(g_df)]
#chroms['seq'] = ''
#
#for i, row in chroms.iterrows(): 
#    chroms.at[i, 'seq'] = ''.join(g_df[row['start']:row['end']][0].tolist())
#chroms = chroms.reset_index().drop(['index', 'start', 'end'], axis=1)
#chroms.columns = ['chr', 'seq']
## write 1-line .fa genome
#chroms.to_csv(genome.replace('.fa', '_1line.fa'), sep="\n", index=False, header=False)
# remove '>' from chromosome id
chroms['chr'] = chroms['chr'].str.replace('>', '')

errors = []
annot_errors = []
print('Processing incomplete 5UTRs')
if not skip1:
    for i, row in df.loc[df['Flag'].isin(['-+', '--'])][:3].iterrows():
        annot = a_df.loc[a_df[8].str.contains('ID=gene-{};'.format(row['gene_name']))]
        if len(annot) < 1:
            annot_errors.append(i)
            continue
        elif len(annot) > 1:
            import pdb; pdb.set_trace()
        annot = annot.iloc[0]
        strand = annot[6]
        if strand == '+':
            chrom = chroms.loc[chroms['seq'].str.contains(row['Sequence'][:min(20, len(row['Sequence']))])]
            if len(chrom) < 1:
                errors.append(i)
                print('error: seq not found', i)
                continue
            if len(chrom) > 1:
                for s in range(50, min(len(row['Sequence']), 500), 50):
                    chrom = chroms.loc[chroms['seq'].str.contains(row['Sequence'][:s])]
                    if len(chrom) == 1:
                        break
                    if len(chrom) == 0:
                        print('Sequence not found: {}'.format(row['Sequence'][:20]))
                        print(i)
                        break
                if len(chrom) > 1:
                    # then we take the first one
                    print('Sequence found more than once: {}'.format(row['Sequence'][:s]))
                    print(i)
            if len(chrom) == 0:
                continue
            chrom = chrom.iloc[0]
            chr = chrom['chr']
            chr_seq = chrom['seq']
            pos = chr_seq.index(row['Sequence'][:min(20, len(row['Sequence']))])
            offset = 100 - row['5UTR_length']
            minus100_pos = pos - offset
            end_pos = len(row['Sequence']) + offset
            new_seq = chr_seq[minus100_pos:minus100_pos+end_pos]
            df.at[i,'Sequence'] = new_seq
            df.at[i, 'Flag'] = '+' + row['Flag'][1]
        else: # if strand == '-':
    #        chrom = chroms.loc[chroms['chr'] == chr]
    #        if len(chrom) != 1:
    #            import pdb; pdb.set_trace()
    #        chrom = chrom.iloc[0]
    #        seq = chrom['seq']
    #        # I am lost
    #        # sequence from the annotation does not match the sequence from df. Why?
    #        # lengths of gene also don't match. 
    #        import pdb; pdb.set_trace()
            rev_sequence = reverse_complement(row['Sequence'][-20:]) 
            chrom = chroms.loc[chroms['seq'].str.contains(rev_sequence)]
            if len(chrom) < 1:
                 errors.append(i)
                 continue
            if len(chrom) > 1:
                for s in range(-50, -1*(min(len(row['Sequence']), 500)), -50):
                    rev_sequence = reverse_complement(row['Sequence'][s:])
                    chrom = chroms.loc[chroms['seq'].str.contains(rev_sequence)]
                    if len(chrom) == 1:
                        break
                    if len(chrom) == 0:
                        print('Sequence not found: {}'.format(rev_sequence))
                        print(i)
                        break
                if len(chrom) > 1:
                    print('Sequence found more than once: {}'.format(rev_sequence))
                    print(i)
            if len(chrom) == 0:
                continue
            chrom = chrom.iloc[0]
            chr_seq = chrom['seq']
            chr = chrom['chr']
            rev_pos = chr_seq.index(rev_sequence) + len(rev_sequence)
            offset = 100 - row['5UTR_length']
            start_pos = rev_pos - offset
            end_pos = rev_pos
            anti_seq = chr_seq[start_pos:end_pos]
            new_seq = row['Sequence'] + reverse_complement(anti_seq)
            df.at[i, 'Sequence'] = new_seq
            df.at[i, 'Flag'] = '+' + row['Flag'][1]
        # rev20 = reverse_complement(row['Sequence'][-20:])
        # rev40 = reverse_complement(row['Sequence'][-40:])
        # seq.index(rev20) = seq.index(rev40) - the same! So, we take new_pos as seq.index(rev20) - (100 - row['5UTR_length'])
        # then add_seq = seq[new_pos:seq.index(rev20)]

    df.to_csv('/icgc/dkfzlsdf/analysis/OE0532/static/elongation/hg38/mRNA.step1.tsv', sep="\t", index=False)

print('-+ and -- are done')

print('Proceeding with +-')
for i, row in df.loc[df['Flag'].isin(['+-'])].iterrows():
    annot = a_df.loc[a_df[8].str.contains('ID=gene-{};'.format(row['gene_name']))]
    if len(annot) < 1:
        annot_errors.append(i)
        continue
    elif len(annot) > 1:
        import pdb; pdb.set_trace()
    annot = annot.iloc[0]
    strand = annot[6]
    if strand == '+':
        chrom = chroms.loc[chroms['seq'].str.contains(row['Sequence'][:min(20, len(row['Sequence']))])]
        if len(chrom) < 1:
            errors.append(i)
        if len(chrom) > 1:
            for s in range(50, min(len(row['Sequence']), 500), 50):
                chrom = chroms.loc[chroms['seq'].str.contains(row['Sequence'][:s])]
                if len(chrom) == 1:
                    break
                if len(chrom) == 0:
                    print('seq not found: {}'.format(rev_sequence))
                    print(i)
                    break
            if len(chrom) > 1:
                print('Sequence found more than once: {}'.format(row['Sequence'][:s]))
                print(i)
        if len(chrom) == 0:
            continue
        chrom = chrom.iloc[0]
        chr = chrom['chr']
        chr_seq = chrom['seq']
        pos = chr_seq.index(row['Sequence'][-20:]) + 20
        offset = 100 - row['3UTR_length']
        end_pos = pos + offset
        new_seq = row['Sequence'] + chr_seq[pos:end_pos]
        df.at[i, 'Sequence'] = new_seq
        df.at[i, 'Flag'] = '++'
    elif strand == '-':
        rev_sequence = reverse_complement(row['Sequence'][:20])
        chrom = chroms.loc[chroms['seq'].str.contains(rev_sequence)]
        if len(chrom) > 1:
            for s in range(50, min(len(row['Sequence']), 500), 50):
                chrom = chroms.loc[chroms['seq'].str.contains(row['Sequence'][:s])]
                if len(chrom) == 1:
                    break
                if len(chrom) == 0:
                    print('seq not found: {}'.format(rev_sequence))
                    print(i)
                    break
            if len(chrom) > 1:
                print('Sequence found more than once: {}'.format(rev_sequence))
                print(i)
        if len(chrom) == 0:
            continue
        chrom = chrom.iloc[0]
        chr = chrom['chr']
        chr_seq = chrom['seq']
        pos = chr_seq.index(rev_sequence)
        offset = 100 - row['3UTR_length']
        start_pos = pos - offset
        end_pos = pos
        new_seq = reverse_complement(chr_seq[start_pos:end_pos]) + row['Sequence']
        df.at[i,'Sequence'] = new_seq
        df.at[i, 'Flag'] = '++'

df = df.drop(annot_errors)
df = df.drop(df.loc[df['Flag'] != '++'].index)
df['gene_name'] = ">" + df['gene_name']
print('Writing file: {}'.format(outfile))
df[['gene_name', 'Sequence']].to_csv(outfile, sep="\n", header=False, index=False)

out2 = outfile + ".df"
print('Writing file: {}'.format(out2))
df.to_csv(out2, sep="\t", index=False)
