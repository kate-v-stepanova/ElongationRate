import sys
import pandas as pd

infile = sys.argv[1]
outfile = sys.argv[2]

g_df = pd.read_csv(infile, sep="\n")
chroms = g_df.loc[g_df[0].str.startswith('>')]
chroms['start'] = chroms.index + 1
chroms['end'] = chroms['start'].tolist()[1:] + [len(g_df)]
chroms['seq'] = ''
for i, row in chroms.iterrows():
    chroms.at[i, 'seq'] = ''.join(g_df[row['start']:row['end']][0].tolist())
chroms = chroms.reset_index().drop(['index', 'start', 'end'], axis=1)
chroms.columns = ['chr', 'seq']
print('Writing file: {}'.format(outfile))
chroms.to_csv(outfile, sep="\n", index=False, header=False)
