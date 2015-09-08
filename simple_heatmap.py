#!/usr/bin/env python
"""
2/19/14 JZL simple_heatmap.py

This script reads a tab-delimited otu table file containing relative abundance and makes a simple
heatmap of this data.  The tab-delimited otu is of raw counts.  The program will compute relative abundance
and then determine which OTUs meet the n-ton cutoff and artificially set the 
abundance so that the heat square shows up as a different color in the color map, highlighting these OTUs, or eliminate.
   
usage:
python simple_heatmap.py -i input_otutable.txt -o output_file.pdf -n cutoff_int -X

otutable file format (blank denotes zero):
sample   In.1    In.3    In.4    
meta    3/19/08 4/30/09 1/30/08 
taxon1    0       0       0
taxon2    1       0       29
taxon3    0       0       0
taxon4    0       0       0
taxon5    0       0       5

"""

"""------------------------------------------------------------------------------------------"""
"""Functions & Declarations"""

from string import strip
from optparse import OptionParser
import csv
from numpy import divide,log10,arange
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
from matplotlib.ticker import FuncFormatter

"""------------------------------------------------------------------------------------------"""
# setup command line arguments
print "Running..."

if __name__ == '__main__':
    parser = OptionParser(usage = "usage: simple_heatmap.py -i input_otutable.txt -o output_file.pdf -n cutoff_int -X",
                  description='2/19/14 JZL simple_heatmap.py')
    parser.add_option("-i", "--input_otutable", action="store", type="string", dest="inputfilename",
                  help="otu table file name (see docstring)")
    parser.add_option("-o", "--output_pdf (optional)", action="store", type="string", dest="outputfilename",
                  help="output pdf name", default=None)
    parser.add_option("-n", "--n_ton_cutoff", action="store", type="float", dest="ntoncutoff",
                  help="singleton, doubleton, etc cutoff", default=5)                                    
    parser.add_option("-X", "--excludeflag", action="store_true", dest="excludeflag", default=False,
                  help="use to exclude OTUs of the n_ton_cutoff rather than highlight")                  
    (options, args) = parser.parse_args()

    mandatories = ["inputfilename"]
    for m in mandatories:
        if not options.__dict__[m]:
            print "\nError: Missing Arguments\n"
            parser.print_help()
            exit(-1)
    
    # read in command line args and parse file
    inputfilename = options.inputfilename
    outputfilename = options.outputfilename
    ntoncutoff = options.ntoncutoff
    excludeflag = options.excludeflag
                
    infile = open(inputfilename, 'U')
    reader = csv.reader(infile, dialect='excel-tab')
    
    sample_name = reader.next()
    sample_meta = reader.next()
    data =[]
    taxa_labels = []
    
    for line in reader:
        taxa_labels.append(line.pop(0))
        data.append(map(float,line))
    taxa_labels = taxa_labels[2:]
    infile.close()
    
    # compute total seq / sample
    sample_totals = []
    sample_cutoff = []
    for i, sample in enumerate(zip(*data)):
        sumsample = sum(sample)
        sample_totals.append(sumsample)
        if ntoncutoff < 1:
            sample_cutoff.append(ntoncutoff)
        else:
            sample_cutoff.append(ntoncutoff/sumsample)
        
    # the artificial abund for marked samples
    highlight_abund = 1.0
    
    rel_data = []
    used_taxa_labels = []
    #set relative abundances
    for line, taxon_label in zip(data, taxa_labels):
        rel_data_row = list(divide(line, sample_totals))
        cutoff_rel_data_row = []
        #check if n-ton cutoff, if so, replace with highlight abund, otherwise, append rel_abund
        for rel_abund, min_cutoff in zip(rel_data_row, sample_cutoff):
            if rel_abund <= min_cutoff and rel_abund > 0:
                #check if we want to include or exclude
                if not excludeflag:
                    cutoff_rel_data_row.append(highlight_abund)
                else:
                    cutoff_rel_data_row.append(float(0))
            else:
                cutoff_rel_data_row.append(rel_abund)
        #to save space, if nothing is there don't add it in
        if sum(cutoff_rel_data_row) > 0:
            used_taxa_labels.append(taxon_label)
            rel_data.append(log10(cutoff_rel_data_row))
    
    # box plot these scores
    print "Plotting..."

    """# a blue-black with red highlights
    cdict = {'red': ((0.0, 1.0, 1.0),
                     (.0000001, .42, .42),
                     (.99, 0.0, 0.0),
                     (1.0, 0.95, 0.95)),
            'green':((0.0, 1.0, 1.0),
                     (.0000001, .68, .68),
                     (.99, 0.0, 0.0),
                     (1.0, 0.9, 0.9)),
            'blue': ((0.0, 1.0, 1.0),
                     (.0000001, .84, .84),
                     (.99, 0.0, 0.0),
                     (1.0, 0.9, 0.9))}"""
                     
    """# a orange-red with blue highlights
    cdict = {'red': ((0.0, 1.0, 1.0),
                     (.000001, 0.99, 0.99),
                     (.9, 0.99, 0.99),
                     (1.0, 0.9, 0.9)),
            'green':((0.0, 1.0, 1.0),
                     (.000001, 0.75, 0.75),
                     (.9, 0.0, 0.0),
                     (1.0, 0.9, 0.9)),
            'blue': ((0.0, 1.0, 1.0),
                     (.000001, 0.55, 0.55),
                     (.9, 0.0, 0.0),
                     (1.0, 0.95, 0.95))}"""
                     
    # a orange-red-blue with blue highlights
    cdict = {'red': ((0.0, 1.0, 1.0),
                     (.000001, 0.99, 0.99),
                     (.3, 0.99, 0.99),
                     (.99, 0.0, 0.0),
                     (1.0, 0.9, 0.9)),
            'green':((0.0, 1.0, 1.0),
                     (.000001, 0.75, 0.75),
                     (.3, 0.0, 0.0),
                     (.99, 0.0, 0.0),
                     (1.0, 0.9, 0.9)),
            'blue': ((0.0, 1.0, 1.0),
                     (.000001, 0.55, 0.55),
                     (.3, 0.0, 0.0),
                     (.99, 0.99, 0.99),
                     (1.0, 0.95, 0.95))}
                     
    my_cmap = colors.LinearSegmentedColormap('my_colormap',cdict,5120)
    num_coords = 90  
    im = plt.imshow(rel_data[::-1], interpolation="nearest", cmap=my_cmap, origin='lower', extent=[-num_coords/3*2,num_coords/3*2,-num_coords/2,num_coords/2])
    plt.colorbar()
    taxa_coords = used_taxa_labels[-2::-int(len(used_taxa_labels)/num_coords)]
    tick_coords = range(-num_coords/2,num_coords/2)
    im.axes.yaxis.set_ticks(tick_coords)
    im.axes.yaxis.set_ticklabels(taxa_coords[1:])
    xticks = arange(-num_coords/3*2,num_coords/3*2,float(num_coords/3*4)/len(sample_meta))
    im.axes.xaxis.set_ticks(xticks)
    im.axes.xaxis.set_ticklabels(sample_meta, rotation=90)
    if not (outputfilename == None):
        print 'Saving ' + outputfilename
        plt.savefig(outputfilename, format='pdf',dpi=300, transparent=True)
    plt.show()
    
    
    print "Done!"