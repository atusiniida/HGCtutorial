import os
import sys
import subprocess
import time

argv = sys.argv
if len(argv) != 3:
    print('Usage: # python ' + argv[0] + ' filename numberOfJobs')
    quit()

inFile = argv[1]
n = int(argv[2])

reference = "ref/ecoli_index"


# define a function for running a command
# return an string output by the command or None when the command fails
def run(command):
    try:
        return subprocess.run(command, shell=True,
                              check=True, stdout=subprocess.PIPE)\
                              .stdout.decode('utf-8')
    except Exception as e:
        sys.stdout.write(str(e) + "\n")
        return None


# split fastq file
fileIndex = 0
lineIndex = 0

totalLineNumber = int(run("wc " + inFile).strip().split()[0])
maxLineNumber = int(totalLineNumber/n)
# maxLineNumber must be devided evenly by 4
maxLineNumber = int(maxLineNumber/4)*4

pid = os.getpid()  # get process id
prefix = "tmp" + str(pid)
fastqFile = prefix + "." + str(fileIndex) + ".fastq"

IN = open(inFile)
OUT = open(fastqFile, "w")
line = IN.readline()
while line:
    if lineIndex == maxLineNumber:
        OUT.close()
        fileIndex = fileIndex + 1
        lineIndex = 0
        fastqFile = prefix + "." + str(fileIndex) + ".fastq"
        OUT = open(fastqFile, "w")
    OUT.write(line)
    lineIndex = lineIndex + 1
    line = IN.readline()
OUT.close()
IN.close()

# submit jobs
maxFileIndex = fileIndex
for fileIndex in range(maxFileIndex+1):
    prefix2 = prefix + "." + str(fileIndex)
    qsub = "qsub -N  " + prefix2 + " bwa.sh " + prefix2 + "  " + reference \
           + " > /dev/null"
    # check whether qsub is succesfly done
    while run(qsub) is None:
            time.sleep(10)

# wait for jobs to finish

tmp = 1
while tmp > 0:
    time.sleep(1)
    tmp = run("qstat | grep  " + prefix + " | wc")
    tmp = int(tmp.strip().split()[0])

# print sam
for fileIndex in range(maxFileIndex+1):
    samFile = prefix + "." + str(fileIndex) + ".sam"
    IN = open(samFile)
    line = IN.readline()
    # take headers　only for the first file
    if fileIndex > 0:
        while line.startswith('@'):
            line = IN.readline()
    while line:
        sys.stdout.write(line)
        line = IN.readline()
    IN.close()

# remove tmp files
run("rm " + prefix + "*")
