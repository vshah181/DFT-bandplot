# DFT Bandplot
Some simple python scripts to plot bandstructures from DFT programmes.
So far we have vasp_bandplot.py (for VASP) and qe_bandplot.py (for QuantumESPRESSO).
We will implement others as we go (if they are needed).


## QuantumESPRESSO
We assume that ```pw.x``` and ```bands.x``` have been successfully run and that the gnuplot file has also been generated as a post-processing step.
Here is a sample input file:
#### INPUT.qebp
    seedname     CoSi
    fermi_level  17.3456
    figsize      6.0 4.0
    klabels      Γ X M Γ R X
    yrange       -5 2 !Plot from 5 eV below Fermi energy to 2 eV above Fermi energy
    colour       tab:purple  !Or define a colour (eg #6463fa)
    filband      CoSi_band.dat.gnu
    ppfile       pp.band.CoSi.out
The filename does not matter. I have called it ```INPUT.qebp``` just as an example. The porgramme is invoked by typing:
```python qe_bandplot.py < INPUT.qebp```.
The output file (in this example) will be called CoSi_EIGENVAL.pdf. 

## VASP
Again we assume that a self-consistent and band-structure calculation have been successfully performed. We require the OUTCAR and EIGENVAL files from the band-structure calculations
#### INPUT.vasp
    fermi_level  17.3456
    figsize      6.0 4.0
    klabels      Γ X M Γ R X
    yrange       -0.5 1.2 !Plot from 0.5 eV below Fermi energy to 1.2 eV above Fermi energy
    colour       tab:purple  !Or define a colour (eg #6463fa)
The filename does not matter. I have called it ```INPUT.vasp``` just as an example. The porgramme is invoked by typing:
```python vasp_bandplot.py < INPUT.vasp```.
The output file will be called EIGENVAL.pdf as VASP doesn't care about any seedname. 

## Dependency list
- Python $\geq$ 3.7.2
- Numpy
- Matplotlib
- Arial font
