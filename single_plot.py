import pandas as pd
import sys
import glob
import os
import matplotlib.pyplot as plt

project_id = sys.argv[1]
subset = ''
if len(sys.argv) >= 3:
    subset = "_{}".format(sys.argv[2])

indir = "/icgc/dkfzlsdf/analysis/OE0532/{}/analysis/output/elongation/results".format(project_id)
plot_dir = "/icgc/dkfzlsdf/analysis/OE0532/{}/analysis/figures/elongation".format(project_id)
metafile = "/icgc/dkfzlsdf/analysis/OE0532/{}/analysis/input/metadata/elongation_table{}.txt".format(project_id, subset)
meta_df = pd.read_csv(metafile, sep="\t")
groups = meta_df['group'].unique().tolist()

os.makedirs(plot_dir, exist_ok=True)

full_df = None
colors = ['deepskyblue', 'deeppink', 'turquoise', 'tomato', 'mediumslateblue', ]
colors = ['#3CB371', '#008B8B', '#00CED1', '#6B8E23', '#5F9EA0', '#4682B4', '#1E90FF']
colors = ['#66c3a5', '#ffffb4', '#bebadb', '#fb8173', '#80b1d3', '#fdb462', '#b3de6a', '#fccde5', '#d9d9d9', '#bc80be', '#ccebc5', '#ffee6f', '#15bfd0', '#bcbd23', '#bc80be', '#c7c7c7', '#f8b6d2', '#c49d94', '#c6b1d6', '#ff9896', '#98e08a', '#ffbb78', '#afc7e8']
color = 0
for group in groups:
    infiles = glob.glob("{}/*{}*_density_plot.txt".format(indir, group))
    group_df = None
    for f in infiles:
        fn = os.path.basename(f).replace('_density_plot.txt', '')
        df = pd.read_csv(f, header=None, names=[fn])
        df['x'] = df.index
#        plt.plot(df['x'], df[fn], color=colors[color], alpha=0.2, label='_nolegend_')
#        plt.ylim(0,3)
        if group_df is None:
            group_df = df
        else:
            group_df = pd.merge(group_df, df, on='x')
    group_df[group] = group_df.drop('x', axis=1).mean(axis=1)
    line = plt.plot(group_df['x'], group_df[group], color=colors[color], linewidth=1, label=group)
    color += 1

plt.rcParams["figure.figsize"] = (10,5)
plt.ylim(0,3)
plt.tight_layout()
plt.legend()
outfile = "{}/all{}.pdf".format(plot_dir, subset)
print('Writing file: {}'.format(outfile))
plt.savefig(outfile)
import pdb; pdb.set_trace()

