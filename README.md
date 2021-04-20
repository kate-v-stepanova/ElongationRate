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

4. Download annotation: `wget https://ftp.ncbi.nih.gov/genomes/refseq/vertebrate_mammalian/Homo_sapiens/latest_assembly_versions/GCF_000001405.39_GRCh38.p13/GCF_000001405.39_GRCh38.p13_genomic.gff.gz`

Unzip & rename: `gzip -d GCF_000001405.39_GRCh38.p13_genomic.gff.gz & mv GCF_000001405.39_GRCh38.p13_genomic.gff GRCh38.p13.gff3`

Customize genome annotation: `python /icgc/dkfzlsdf/analysis/OE0532/software/ElongationRate/discard_extrachromosomal_annotation.py /icgc/dkfzlsdf/analysis/OE0532/static/elongation/hg38/GRCh38.p13.gff3 /icgc/dkfzlsdf/analysis/OE0532/static/elongation/hg38/GRCh38.p13.custom.gff3 hg`

Customize annotation 2:

```
python /icgc/dkfzlsdf/analysis/OE0532/software/ElongationRate/discard_gnomon_annotation.py /icgc/dkfzlsdf/analysis/OE0532/static/elongation/hg38/GRCh38.p13.custom.gff3 /icgc/dkfzlsdf/analysis/OE0532/static/elongation/hg38/GRCh38.p13.Refseq.gff
```

Discard non-coding: `Rscript /icgc/dkfzlsdf/analysis/OE0532/software/ElongationRate/Discard_noncoding_annotation.r /icgc/dkfzlsdf/analysis/OE0532/static/elongation/hg38/GRCh38.p13.Refseq.gff /icgc/dkfzlsdf/analysis/OE0532/static/elongation/hg38/GRCh38.p13.Refseq.coding.gff`

8. Convert gff to gtf

Get gffread: `git clone https://github.com/gpertea/gffread.git`

cd: `cd /icgc/dkfzlsdf/analysis/OE0532/software/gffread`

Build: `make release`

Convert: `/icgc/dkfzlsdf/analysis/OE0532/software/gffread/gffread /icgc/dkfzlsdf/analysis/OE0532/static/elongation/hg38/GRCh38.p13.Refseq.coding.gff -T -o /icgc/dkfzlsdf/analysis/OE0532/static/elongation/hg38/GRCh38.p13.Refseq.coding.gtf`

10. Fetch all mRNA records: `bsub -R "rusage[mem=30G]" perl /icgc/dkfzlsdf/analysis/OE0532/software/ElongationRate/mRNA_extractor.pl /icgc/dkfzlsdf/analysis/OE0532/static/elongation/GRCm38.p6.rna.gbk`

This will output temp1, temp2 and temp3 files in the current directory. `temp3` will be used for the next step.

Add missing sequences if 5UTR and 3UTR length <100: `bsub -q long -R "rusage[mem=100G]" python mRNA_genome_filler.py temp3 GRCh38.p13.genome_1line.fa GRCh38.p13.Refseq.coding.gff mRNA_100.fa` 

