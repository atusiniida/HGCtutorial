import sys
import subprocess

argv = sys.argv
if len(argv) != 4:
    print('Usage: # python ' + argv[0] +
          ' inputFastaqFileName numberOfSplitFiles prefixOfSplitFiles')
    quit()

inFile = argv[1]
n = int(argv[2])
prefix = argv[3]


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
