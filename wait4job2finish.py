import sys
import subprocess
import time

argv = sys.argv
if len(argv) != 2:
    print('Usage: # python ' + argv[0] + ' jobID ')
    quit()

prefix = argv[1]


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


tmp = 1
while tmp > 0:
    time.sleep(1)
    tmp = run("qstat | grep  " + prefix + " | wc")
    tmp = int(tmp.strip().split()[0])
print("jobs have finished!")
