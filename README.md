# DFT Bandplot
Some simple python scripts to plot bandstructures from DFT programmes.
So far we have vasp_bandplot.py (for VASP) and qe_bandplot.py (for QuantumESPRESSO).
We will implement others as we go (if they are needed).


## QuantumESPRESSO
We assume that ```pw.x``` and ```bands.x``` have been successfully run and that the gnuplot file has also been generated as a post-processing step.
Here is a sample input file:
#### INPUT.qebp
    seedname CoSi
    e_fermi  17.3456
    figsize  6.0 4.0
    klabels  Γ X M Γ R X
    yrange   11 23
    colour   tab:purple  !Or define a colour (eg #6463fa)
    filband  CoSi_band.dat.gnu
    ppfile   pp.band.CoSi.out
The filename does not matter. I have called it ```INPUT.qebp``` just as an example. The porgramme is invoked by typing:
```python vasp_bandplot.py < INPUT.qebp```.

## Dependency list
- Python $\geq$ 3.7.2
- Numpy
- Matplotlib
- Arial font
