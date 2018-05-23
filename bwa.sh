#!/bin/bash
#$ -S /bin/bash
#$ -cwd

#qsub bwa.sh read10000 ref/ecoli_index

PREFIX=$1 # read10000
REFFILE=$2 # ref/ecoli_index

bwa-0.7.12/bwa mem  ${REFFILE}   ${PREFIX}.fastq > ${PREFIX}.sam
#bwa-0.7.12/bwa mem  read10000   read10000.fastq > read10000.sam

#bwa-0.7.12/bwa aln ${REFFILE} ${PREFIX}.fastq > ${PREFIX}.sai
#bwa-0.7.12/bwa samse ${REFFILE} ${PREFIX}.sai ${PREFIX}.fastq > ${PREFIX}.sam
