import sys
import subprocess

argv = sys.argv
if len(argv) <= 1:
    print('Usage: # python ' + argv[0] + ' command')
    quit()

command = " ".join(argv[1:])


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


output = run(command)
if output is None:
    print("The command failed!")
else:
    print(output.rstrip())
