file = open("EMG.csv", 'r')
out = open("EMGmodify.csv", 'w')

while True:
    line = file.readline()
    line = str(line)
    if line.find('\n') > 0:
        out.write(line)
    elif line.find('\n') == 0:
        continue
    else:
        break
