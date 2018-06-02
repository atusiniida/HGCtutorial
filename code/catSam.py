import sys

argv = sys.argv
if len(argv) < 2:
    print('Usage: # python ' + argv[0] + ' samFiles ')
    quit()

samFiles = argv[1:]

# print sam
first = True
for samFile in samFiles:
    IN = open(samFile)
    line = IN.readline()
    # take headers　only for the first file
    if not first:
        while line.startswith('@'):
            line = IN.readline()
    while line:
        print(line.rstrip())
        line = IN.readline()
    IN.close()
    first = False
