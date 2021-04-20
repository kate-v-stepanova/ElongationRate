import pandas as pd
import sys

infile = sys.argv[1]
outfile = infile
if len(sys.argv) >= 3:
    outfile = sys.argv[2]

df = pd.read_csv(infile, sep="\n", header=None)
df.columns = ['b']
b = df.loc[df['b'].str.startswith('>'), 'b']
b = b.str.split(' ').str[0]
df.loc[df['b'].str.startswith('>'), 'b'] = b
print('Writing file: {}'.format(outfile))
df.to_csv(outfile, sep="\n", header=False, index=False)
