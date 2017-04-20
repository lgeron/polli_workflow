import pandas as pd
import sys
import re

file = sys.argv[1]
l1 = re.findall(r'(.*)-', file)
l2 = re.findall(r'-(.*).csv', file)
print('{}'.format(l1[0]))
print('{}'.format(l2[0]))

df = pd.read_csv(file)

cols = df.columns.tolist()

assert len(cols) == 2, "CSV did not have 2 columns, please input in L1,L2 format"

with open('L1.txt', 'w') as file:
    for line in df[cols[0]]:
        file.write(line)
        file.write('\n')

with  open('L2.txt', 'w') as file:
    for line in df[cols[1]]:
        file.write(line)
        file.write('\n')
