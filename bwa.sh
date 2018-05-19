#!/bin/bash
#$ -S /bin/bash
#$ -cwd

PREFIX=$1
REFFILE=$2

#bwa-0.7.12/bwa mem  ${REFFILE}   ${PREFIX}.fastq > ${PREFIX}.sam

bwa-0.7.12/bwa aln ${REFFILE} ${PREFIX}.fastq > ${PREFIX}.sai
bwa-0.7.12/bwa samse ${REFFILE} ${PREFIX}.sai ${PREFIX}.fastq > ${PREFIX}.sam
