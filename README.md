# ElongationRate
The original analysis is taken from here: https://github.com/germaximus/ElongationRate and adjusted for the human data.

Reference genome is downloaded from here: `https://ftp.ncbi.nih.gov/genomes/refseq/vertebrate_mammalian/Homo_sapiens/latest_assembly_versions/GCF_000001405.39_GRCh38.p13/`

1. Download rna fasta: `wget https://ftp.ncbi.nih.gov/genomes/refseq/vertebrate_mammalian/Homo_sapiens/latest_assembly_versions/GCF_000001405.39_GRCh38.p13/GCF_000001405.39_GRCh38.p13_rna.fna.gz`

2. Download genome: `for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22; do echo "wget https://ftp.ncbi.nih.gov/genomes/refseq/vertebrate_mammalian/Homo_sapiens/all_assembly_versions/GCF_000001405.39_GRCh38.p13/GCF_000001405.39_GRCh38.p13_assembly_structure/Primary_Assembly/assembled_chromosomes/FASTA/chr$i.fna.gz"; done`

Merge chromosomes into one file: `cat chr* > GRCh38.p13.genome.fa.gz`

Unzip: `gzip -d GRCh38.p13.genome.fa.gz`

Delete: `rm chr*.gz`

3.  Fix headers

Original header: `>NC_000001.11 Homo sapiens chromosome 1, GRCh38.p13 Primary Assembly`

We want to keep: `>NC_000001.11`

Fix header genome: `python fix_header.py GRCh38.p13.genome.fa.`

Fix header rna: `python fix_header.py GRCh38.p13_rna.fna`

4. Download .gbk: `wget https://ftp.ncbi.nih.gov/genomes/refseq/vertebrate_mammalian/Homo_sapiens/latest_assembly_versions/GCF_000001405.39_GRCh38.p13/GCF_000001405.39_GRCh38.p13_rna.gbff.gz`

Unzip: `gzip -d /icgc/dkfzlsdf/analysis/OE0532/static/elongation/hg38/GCF_000001405.39_GRCh38.p13_rna.gbff.gz`

Rename: `mv /icgc/dkfzlsdf/analysis/OE0532/static/elongation/hg38/GCF_000001405.39_GRCh38.p13_rna.gbff /icgc/dkfzlsdf/analysis/OE0532/static/elongation/hg38/GRCh38.p13.rna.gbk`

5. Download annotation: `wget https://ftp.ncbi.nih.gov/genomes/refseq/vertebrate_mammalian/Homo_sapiens/latest_assembly_versions/GCF_000001405.39_GRCh38.p13/GCF_000001405.39_GRCh38.p13_genomic.gff.gz`

Unzip & rename: `gzip -d GCF_000001405.39_GRCh38.p13_genomic.gff.gz & mv GCF_000001405.39_GRCh38.p13_genomic.gff GRCh38.p13.gff3`

Customize genome annotation: `python /icgc/dkfzlsdf/analysis/OE0532/software/ElongationRate/discard_extrachromosomal_annotation.py /icgc/dkfzlsdf/analysis/OE0532/static/elongation/hg38/GRCh38.p13.gff3 /icgc/dkfzlsdf/analysis/OE0532/static/elongation/hg38/GRCh38.p13.custom.gff3 hg`

Customize annotation 2:

```
python /icgc/dkfzlsdf/analysis/OE0532/software/ElongationRate/discard_gnomon_annotation.py /icgc/dkfzlsdf/analysis/OE0532/static/elongation/hg38/GRCh38.p13.custom.gff3 /icgc/dkfzlsdf/analysis/OE0532/static/elongation/hg38/GRCh38.p13.Refseq.gff
```

Discard non-coding: `Rscript /icgc/dkfzlsdf/analysis/OE0532/software/ElongationRate/Discard_noncoding_annotation.r /icgc/dkfzlsdf/analysis/OE0532/static/elongation/hg38/GRCh38.p13.Refseq.gff /icgc/dkfzlsdf/analysis/OE0532/static/elongation/hg38/GRCh38.p13.Refseq.coding.gff`

6. Convert gff to gtf

Get gffread: `git clone https://github.com/gpertea/gffread.git`

cd: `cd /icgc/dkfzlsdf/analysis/OE0532/software/gffread`

Build: `make release`

Convert: `/icgc/dkfzlsdf/analysis/OE0532/software/gffread/gffread /icgc/dkfzlsdf/analysis/OE0532/static/elongation/hg38/GRCh38.p13.Refseq.coding.gff -T -o /icgc/dkfzlsdf/analysis/OE0532/static/elongation/hg38/GRCh38.p13.Refseq.coding.gtf`

7. Fetch all mRNA records: `bsub -R "rusage[mem=30G]" perl /icgc/dkfzlsdf/analysis/OE0532/software/ElongationRate/mRNA_extractor.pl /icgc/dkfzlsdf/analysis/OE0532/static/elongation/GRCm38.p6.rna.gbk`

This will output temp1, temp2 and temp3 files in the current directory. `temp3` will be used for the next step.

Add missing sequences if 5UTR and 3UTR length <100: `bsub -q long -R "rusage[mem=100G]" python mRNA_genome_filler.py temp3 GRCh38.p13.genome_1line.fa GRCh38.p13.Refseq.coding.gff mRNA_100.fa` 

8. Blastdb

Download and install from here: https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/

build a database with local sequences: `/usr/local/ncbi/blast/bin/makeblastdb -in mRNA_100.fa -title "mRNA_100" -dbtype nucl`

blast all sequences against each other: `/usr/local/ncbi/blast/bin/blastn -task blastn -num_threads 4 -outfmt 6 -evalue 0.001 -db mRNA_100.fa -query mRNA_100.fa -out blast_result.txt`

`perl BLASTNprocessor.pl blast_result.txt`

9. Mapping ribosomal footprints to unique ORFs

Build reference: `bsub -q long -R "rusage[mem=30G]" /icgc/dkfzlsdf/analysis/OE0532/software/bowtie-1.2.3-linux-x86_64/bowtie-build /icgc/dkfzlsdf/analysis/OE0532/static/elongation/mRNA_100.fasta /icgc/dkfzlsdf/analysis/OE0532/static/elongation/mRNA_100uniq`

Create uniq.bwt for all samples: `for f in $(ls /icgc/dkfzlsdf/analysis/OE0532/3808/analysis/output/demultiplexed/*.fastq); do fn=$(basename $f); fn=${fn%.fastq}; echo "bsub -R \"rusage[mem=30G]\" -q long /icgc/dkfzlsdf/analysis/OE0532/software/bowtie-1.2.3-linux-x86_64/bowtie -p 20 -v 2 -m 1 --norc --max /icgc/dkfzlsdf/analysis/OE0532/3808/analysis/output/elongation/genomic/$fn.fastq /icgc/dkfzlsdf/analysis/OE0532/static/elongation/hg38/mRNA_100uniq $f \> /icgc/dkfzlsdf/analysis/OE0532/3808/analysis/output/elongation/bowtie/$fn.coverage.bwt"; done`


10. Coverage

Coverage files:
`for f in $(ls bowtie/*.bwt); do fn=$(basename $f); fn=${fn%.bwt}; echo "perl Coverage.pl hg38/mRNA_100.fa $f coverage/${fn}.txt"; done`

Final coverage files (to plot): `for f in $(ls coverage/*.txt); do fn=$(basename $f); fn=${fn%.coverage.txt}; echo "perl Coverage_processor.pl 2000 start $f" results/$fn; done`

11. Plot results
Create a table: `vim /icgc/dkfzlsdf/analysis/OE0532/3808/analysis/input/metadata/elongation_table.txt`

The table looks like that:

```
sample  group
S1_Ctrl_0min    Ctrl
S2_Ctrl_2.5min  Ctrl
S3_Ctrl_5min    Ctrl
S4_Ctrl_10min   Ctrl
S5_STLC_0min    STLC
S6_STLC_2.5min  STLC
S7_STLC_5min    STLC
S8_STLC_10min   STLC
```

Plot results: `python plot_results.py 3808`

Single plot: `python single_plot.py 3808`



