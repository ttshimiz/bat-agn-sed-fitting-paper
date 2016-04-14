import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sn

# Set some plotting parameters
sn.set(context='paper', color_codes=True, style='ticks')
mpl.rcParams['xtick.labelsize'] = 8
mpl.rcParams['ytick.labelsize'] = 8
mpl.rcParams['axes.labelsize'] = 10
mpl.rcParams['legend.fontsize'] = 8
mpl.rcParams['text.usetex'] = True
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = 'Computer Modern Roman'
mpl.rcParams['mathtext.fontset'] = 'cm'
mpl.rcParams['ps.fonttype'] = 42                         # Make sure fonts are T1
mpl.rcParams['pdf.fonttype'] = 42

# Define the optimum widths of figures depending if they will be in a column or 
# span the whole page
columnwidth = 240./72.27 # Width of column in LaTeX paper in inches
textwidth = 504./72.27   # Width of text in LaTeX paper in inches

# Directory to save figures
figsave_dir = '../figures/'