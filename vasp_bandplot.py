import numpy as np
import matplotlib.pyplot as plt
import sys

plt.rcParams["font.family"] = "Arial"
plt.rcParams["mathtext.fontset"] = "custom"
plt.rcParams["mathtext.rm"] = "Arial"
plt.rcParams["mathtext.it"] = "Arial:italic"
plt.rcParams["mathtext.bf"] = "Arial:bold"
plt.rcParams['svg.fonttype'] = 'none'


def generate_kdists(kpoints, nkp):
    kdists = np.empty(nkp)
    kdists[0] = 0.0
    for i in range(1, nkp):
        dk = kpoints[i] - kpoints[i-1]
        kdists[i] = kdists[i-1] + np.linalg.norm(dk)
    return kdists


def read_outcar():
    with open('OUTCAR', 'r', encoding='utf-8') as f:
        for line in f:
            split_line = line.split()
            if (len(split_line) > 0 and split_line[0] == 'Generated'):
                kp_per_path = int(split_line[1])
                nkp = int(split_line[11])
                n_h_sym = int(nkp / kp_per_path) + 1
                kpoints = np.empty([nkp, 3])
            elif line.strip() == "Following cartesian coordinates:":
                f.readline()
                for i in range(nkp):
                    split_line = f.readline().split()[:-1]
                    kpoints[i, 0] = float(split_line[0])
                    kpoints[i, 1] = float(split_line[1])
                    kpoints[i, 2] = float(split_line[2])
    return kpoints, nkp, n_h_sym, kp_per_path

def read_master_input():
    for line in sys.stdin:
        split_line = line.split()
        if split_line[0] == 'fermi_level':
            fermi_level = float(split_line[1])
        elif split_line[0] == 'yrange':
            yrange = [float(split_line[1]), float(split_line[2])]
        elif split_line[0] == 'colour':
            colour = split_line[1]
        elif split_line[0] == 'figsize':
            fig_dimensions = (float(split_line[1]), float(split_line[2]))
        elif split_line[0] == 'klabels':
            klabels=split_line[1:]
    return fermi_level, yrange, colour, fig_dimensions, klabels


def read_eigenval(nkp):
    with open('EIGENVAL', 'r', encoding='utf-8') as f:
        for i in range(5):
            f.readline()  # Stuff we don't care about
        num_bands = int(f.readline().split()[-1])
        bands = np.empty([num_bands, nkp])
        for ik in range(nkp):
            f.readline()
            f.readline()
            for ib in range(num_bands):
                bands[ib, ik] = float(f.readline().split()[1])
    return bands


def plot_graph(kdists, bands, xtics, colour, yrange, efermi, fig_dims):
    tic_locs, tic_labels = xtics
    fig = plt.figure(figsize=fig_dims)
    ax = fig.add_subplot(1, 1, 1)
    ax.tick_params(direction='in')
    ax.set_ylabel(r'$E$ (eV)')
    ax.set_xticks(tic_locs, tic_labels)
    ax.set_xlim(np.min(kdists), np.max(kdists))
    ax.set_ylim(np.min(yrange), np.max(yrange))
    ax.vlines(tic_locs, color='#000000', ymin=np.min(yrange),
            ymax=np.max(yrange), linewidth=0.5)
    ax.hlines(efermi, linestyle='dashed', color='#000000', xmin=np.min(kdists),
            xmax=np.max(kdists), linewidth=0.5)
    for band in bands:
        ax.plot(kdists, band, color=colour, linewidth=1.0)
    plt.tight_layout()
    plt.savefig('EIGENVAL.pdf')


def main():
    kpoints, nkp, n_h_sym, kp_per_path = read_outcar()
    efermi, yrange, colour, fig_dims, klabels = read_master_input()
    kdists = generate_kdists(kpoints, nkp)
    tic_locs = kdists[::kp_per_path]
    tic_locs = np.append(tic_locs, kdists[-1])
    xtics = [tic_locs, klabels]
    bands = read_eigenval(nkp)
    plot_graph(kdists, bands, xtics, colour, yrange, efermi, fig_dims)


if __name__ == "__main__":
    main()
