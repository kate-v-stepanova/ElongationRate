import pandas as pd
import sys
import glob
import os
import matplotlib.pyplot as plt

project_id = sys.argv[1]

indir = "/icgc/dkfzlsdf/analysis/OE0532/{}/analysis/output/elongation/results".format(project_id)
plot_dir = "/icgc/dkfzlsdf/analysis/OE0532/{}/analysis/figures/elongation".format(project_id)
metafile = "/icgc/dkfzlsdf/analysis/OE0532/{}/analysis/input/metadata/elongation_table.txt".format(project_id)
meta_df = pd.read_csv(metafile, sep="\t")
groups = meta_df['group'].unique().tolist()

os.makedirs(plot_dir, exist_ok=True)

full_df = None
for group in groups:
    infiles = glob.glob("{}/*{}*_density_plot.txt".format(indir, group))
    plt.rcParams["figure.figsize"] = (10,len(infiles) * 3)
    outfile = "{}/{}.pdf".format(plot_dir, group)
    group_df = None
    fig, ax = plt.subplots(len(infiles),1)
    i = 0
    for f in infiles:
        fn = os.path.basename(f).replace('_density_plot.txt', '')
        df = pd.read_csv(f, header=None, names=[fn])
        df['x'] = df.index
        ax[i].plot(df['x'], df[fn])
        ax[i].title.set_text(fn)
        i += 1
        if group_df is None:
            group_df = df
        else:
            group_df = pd.merge(group_df, df, on='x')
    print('Writing file: {}'.format(outfile))
    plt.tight_layout()
    fig.savefig(outfile)
    group_df[group] = group_df.drop('x', axis=1).mean(axis=1)
    if full_df is None:
        full_df = group_df[['x', group]]
    else:
        full_df = pd.merge(full_df, group_df[['x', group]], on='x')

plt.rcParams["figure.figsize"] = (10,len(groups) * 3)
fig, ax = plt.subplots(len(groups),1)
i = 0
for group in groups:
    ax[i].plot(full_df['x'], full_df[group])
    ax[i].title.set_text("Mean {}".format(group))
    i += 1
plt.tight_layout()
outfile = "{}/mean.pdf".format(plot_dir)
print('Writing file: {}'.format(outfile))
fig.savefig(outfile)
import pdb; pdb.set_trace()


