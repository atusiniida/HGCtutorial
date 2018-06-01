import sys
import subprocess
import time

argv = sys.argv
if len(argv) < 2:
    print('Usage: # python ' + argv[0] + ' fataqFiles ')
    quit()

inFiles = argv[1:]
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


# submit jobs
for f in inFiles:
    prefix = f.replace(".fastq", "")
    qsub = "qsub -N  " + prefix + " bwa.sh " + prefix + "  " + reference \
           + " > /dev/null"
    # check whether qsub is succesfly done
    while run(qsub) is None:
            time.sleep(10)
