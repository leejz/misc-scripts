#!/bin/bash
# simple script to run bowtie2 on a ref and count reads in a gff

ref_path=$1
fq1=$2
fq2=$3
gff=$4
outpath=$5
fn=$(basename $fq1)
prefix=${fn%_R1_001.fastq.gz}
if [ $# -ne 5 ]; then
  echo "invalid number of arguements"
  echo "usage: bowtie2_count.sh ref_path fq1 fq2 gff outpath"
  echo "requires: bowtie2, samtools, bedtools"
  exit
fi

if [ ! -f $fq1 ]; then
  echo "$fq1 not found"
  exit
fi

if [ ! -f $fq2 ]; then
  echo "$fq2 not found"
  exit
fi

if [ ! -f $gff ]; then
  echo "$gff not found"
  exit
fi

if [ ! -f $ref_path.1.bt2 ]; then
  echo "$ref_path not found"
  exit
fi

if [ ! -d $outpath ]; then
  echo "$outpath not found"
  exit
fi

(bowtie2 -p 10 -x $ref_path -1 $fq1 -2 $fq2 | samtools view -h -F 4 | samtools sort -O BAM | bedtools coverage -a $gff -b stdin | cut -f9-11 -d$'\t' | awk -F$'\t'  'BEGIN {OFS=FS} {print $1, $2, $2/$3}') 2>$outpath/$prefix.err.out 1>$outpath/$prefix.cov.txt
