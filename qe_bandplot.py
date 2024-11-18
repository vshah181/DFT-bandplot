import sys
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Arial"
plt.rcParams["mathtext.fontset"] = "custom"
plt.rcParams["mathtext.rm"] = "Arial"
plt.rcParams["mathtext.it"] = "Arial:italic"
plt.rcParams["mathtext.bf"] = "Arial:bold"
plt.rcParams['svg.fonttype'] = 'none'

def read_input():
    for line in sys.stdin:
        split_line = line.split()
        if split_line[0] == 'fermi_level':
            fermi_level = float(split_line[1])
        elif split_line[0] == 'yrange':
            ene_range = (float(split_line[1]), float(split_line[2]))
        elif split_line[0] == 'seedname':
            seedname = split_line[1]
        elif split_line[0] == 'figsize':
            fig_dimensions = (float(split_line[1]), float(split_line[2]))
        elif split_line[0] == 'colour':
            colour=split_line[1]
        elif split_line[0] == 'filband':
            filband=split_line[1]
        elif split_line[0] == 'ppfile':
            ppfile=split_line[1]
        elif split_line[0] == 'klabels':
            klabels = split_line[1:]
    return fermi_level, ene_range, seedname, fig_dimensions, colour, filband,\
            ppfile, klabels


def read_ppfile(ppfile):
    tic_locs = []
    with open(ppfile, 'r', encoding='utf-8') as f:
        for line in f:
            split_line = line.split()
            if split_line[:2] == ['high-symmetry', 'point:']:
                tic_locs.append(float(split_line[-1]))
    return tic_locs


def read_energies(filband):
    data = np.loadtxt(filband)
    klist = np.unique(data[:, 0])
    bands = np.reshape(data[:, 1], (-1, len(klist)))
    return klist, bands


def plot_bands(tic_locs, klabels, e_fermi, klist, bands, size, colour,\
        ene_range, seedname):
    figure_name = seedname+"_EIGENVAL.pdf"
    fig = plt.figure(figsize=size)
    ax = fig.add_subplot(1, 1, 1)
    for iband in range(len(bands)):
        ax.plot(klist, bands[iband, :]-e_fermi, color=colour, linewidth=1.0)
    ax.set_xlim([np.min(klist), np.max(klist)])
    ax.set_ylim(ene_range)
    ax.set_ylabel(r'$E - E_F$ (eV)')
    ax.set_xticks(tic_locs, klabels)
    ax.vlines(tic_locs, color='#000000', ymin=np.min(ene_range),
            ymax=np.max(ene_range), linewidth=0.5)
    ax.hlines(0.00, color='#000000', xmin=np.min(klist), xmax=np.max(klist),
            linewidth=0.5, linestyle='dashed')
    plt.tight_layout()
    plt.savefig(figure_name)

def main():
    fermi_level, ene_range, seedname, fig_dimensions, colour, filband, ppfile,\
            klabels = read_input()
    tic_locs = read_ppfile(ppfile)
    klist, bands = read_energies(filband)
    plot_bands(tic_locs, klabels, fermi_level, klist, bands, fig_dimensions,\
            colour, ene_range, seedname)

if __name__ == '__main__':
    main()
