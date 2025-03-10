import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import sys

plt.rcParams["font.family"] = "Arial"
plt.rcParams["mathtext.fontset"] = "custom"
plt.rcParams["mathtext.rm"] = "Arial"
plt.rcParams["mathtext.it"] = "Arial:italic"
plt.rcParams["mathtext.bf"] = "Arial:bold"
plt.rcParams['svg.fonttype'] = 'none'


def complementary_colour(colour_string):
    r, g, b = mcolors.to_rgb(colour_string)
    complementary_colour = [1.0 - r, 1.0 - g, 1.0 - b]
    return mcolors.to_hex(complementary_colour)


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
    wann_file = ""
    wann_colour = "#ff6978"
    colour = "#6463fa"
    plot_wann = False
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
        elif split_line[0] == 'wann_band':
            wann_file=split_line[1]
            plot_wann = True
        elif split_line[0] == 'wann_colour':
            wann_colour = split_line[1]
    return fermi_level, yrange, colour, fig_dimensions, klabels, plot_wann,\
            wann_file, wann_colour

def read_wannier(filband):
    data = np.loadtxt(filband)
    klist = np.unique(data[:, 0])
    bands = np.reshape(data[:, 1], (-1, len(klist)))
    return klist, bands


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


def plot_compare(kdists, bands, xtics, colour, yrange, efermi, fig_dims,\
        klist_wan, band_wan, wann_colour):
    scale = np.max(kdists) / np.max(klist_wan)
    tic_locs, tic_labels = xtics
    fig = plt.figure(figsize=fig_dims)
    ax = fig.add_subplot(1, 1, 1)
    ax.tick_params(direction='in')
    ax.set_ylabel(r'$E - E_F$ (eV)')
    ax.set_xticks(tic_locs, tic_labels)
    ax.set_xlim(np.min(kdists), np.max(kdists))
    ax.set_ylim(np.min(yrange), np.max(yrange))
    ax.vlines(tic_locs, color='#000000', ymin=np.min(yrange),
            ymax=np.max(yrange), linewidth=0.5)
    ax.hlines(0.0, linestyle='dashed', color='#000000', xmin=np.min(kdists),
            xmax=np.max(kdists), linewidth=0.5)
    for iband in range(len(bands)):
        if iband > 0:
            ax.scatter(kdists, bands[iband, :]-efermi,
                    c=colour, s=8.0, marker='o')
        else: 
            ax.scatter(kdists, bands[iband, :]-efermi, label='VASP',
                    c=colour, s=8.0, marker='o')
    for iband in range(len(band_wan)):
        if iband > 0:
            ax.plot(klist_wan*scale, band_wan[iband, :]-efermi,
                    color=wann_colour, linewidth=1.0)
        else:
            ax.plot(klist_wan*scale, band_wan[iband, :]-efermi, 
                    color=wann_colour, linewidth=1.0, label='Wannier90')
    ax.legend(loc='best')
    plt.tight_layout()
    plt.savefig('COMPARE.pdf')


def plot_graph(kdists, bands, xtics, colour, yrange, efermi, fig_dims):
    tic_locs, tic_labels = xtics
    fig = plt.figure(figsize=fig_dims)
    ax = fig.add_subplot(1, 1, 1)
    ax.tick_params(direction='in')
    ax.set_ylabel(r'$E - E_F$ (eV)')
    ax.set_xticks(tic_locs, tic_labels)
    ax.set_xlim(np.min(kdists), np.max(kdists))
    ax.set_ylim(np.min(yrange), np.max(yrange))
    ax.vlines(tic_locs, color='#000000', ymin=np.min(yrange),
            ymax=np.max(yrange), linewidth=0.5)
    ax.hlines(0.0, linestyle='dashed', color='#000000', xmin=np.min(kdists),
            xmax=np.max(kdists), linewidth=0.5)
    for band in bands:
        ax.plot(kdists, band-efermi, color=colour, linewidth=1.0)
    plt.tight_layout()
    plt.savefig('EIGENVAL.pdf')


def main():
    kpoints, nkp, n_h_sym, kp_per_path = read_outcar()
    efermi, yrange, colour, fig_dims, klabels, plot_wann, \
            wann_file, wann_colour = read_master_input()
    kdists = generate_kdists(kpoints, nkp)
    tic_locs = kdists[::kp_per_path]
    tic_locs = np.append(tic_locs, kdists[-1])
    xtics = [tic_locs, klabels]
    bands = read_eigenval(nkp)
    if plot_wann:
        klist_wan, band_wan = read_wannier(wann_file)
        plot_compare(kdists, bands, xtics, colour, yrange, efermi, fig_dims, \
                klist_wan, band_wan, wann_colour)
    else:
        plot_graph(kdists, bands, xtics, colour, yrange, efermi, fig_dims)


if __name__ == "__main__":
    main()
