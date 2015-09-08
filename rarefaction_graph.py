#!/usr/bin/python
"""This script plots the rarefaction curve with error bars as shaded colors. No files associated"""

"""------------------------------------------------------------------------------------------"""

"""Modules and Libraries"""
#from pylab import *
import matplotlib.pyplot as plt
import numpy as np
import operator
import csv

"""------------------------------------------------------------------------------------------"""
"""Function and Class Definitions"""

def plot_data(ax,xaxis, datalist, color, al, linelist):
"""ax is the figure axis, xaxis is the list of x points (all the same), y is the list of list of y points, /
color is the color scheme set in the main body, al is the alpha opacity,/
linelist is the list of the order of lines to be used in the shaded figure counted in the order in which they are entered./
so [0,2,3] will draw shaded regions for lines 1 and 3, 3 and 4, and ignore line 1, but all lines are drawn too."""

    for i in range(len(linelist)-1):
        botline=linelist[i]
        topline=linelist[i+1]
        ax.fill(xaxis[:len(datalist[botline])]+xaxis[len(datalist[topline])-1::-1], datalist[botline]+datalist[topline][::-1], color, alpha=al)

    for i, plotlist in enumerate(datalist):
        ax.plot(xaxis[:len(plotlist)],plotlist,color,linewidth=1.5)


"""------------------------------------------------------------------------------------------"""
"""Body Section"""
print "Running..."

#raw data
xaxis=[100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,1000,1050,1100,1150,1200,1250,1300,1350,1400,1450,1500,1550,1600,1650,1700,1750,1800,1850,1900,1950,2000,2050,2100,2150,2200,2250,2300,2350,2400,2450,2500,2550,2600,2650,2700,2750,2800,2850,2900,2950,3000,3050,3100,3150,3200,3250,3300,3350,3400,3450,3500,3550,3600,3650,3700,3750,3800,3850,3900,3950,4000,4050,4100,4150,4200,4250,4300,4350,4400,4450,4500,4550,4600,4650,4700,4750,4800,4850,4900]

aeb=[[49.14,64.25,76.77,88.16,98,106.47,114.67,122.01,129.32,135.92,142.42,147.92,152.72],\
[50.1,65.34,76.83,87.77,98.24,106.3,114.64,121.84,129.52,136.58,141.8,147.37,154.51,160.1,165.69,170.71,176.19,180.71,184.63,189.27],\
[50.98,66.16,80.46,91.68,101.63,108.97,118.38,126.32,132.96,140.51,146.69,154.7,160.14,165.63,171.93,177.66,182.35,186.73,191.73,196.4,200.34,204.86,208.77]]

eqbasin=[[14.23,17.51,20.25,21.97,24.1,25.52,27.06,28.39,28.91,30.33,31.25,32.01,32.6,33.55,34.2,34.86,35.12,36.13,36.61,37.06,37.74],\
[17.61,21.57,23.58,26.02,28.11,30.24,31.18,32.65,33.79,35.23,36.03,37.16,37.69,38.75,39.58,40.37],\
[22.14,27.05,29.76,33.08,34.49,36.56,38.27,39.53,41.03,41.56,42.82,43.76,44.83,45.77,46.2,46.96,47.41,48.25,48.95,49.52,50.24,50.76,50.91,51.62,52.42,52.77,53.4,53.76,53.89,54.98,55.54,55.34,55.78,56.76,56.73,57.2,57.48,57.62,58.58,58.71,59.03,59.5,59.68,60.33,60.47,60.85,60.86,61.47,61.54,61.9,62.2,62.44,62.82,63,63.11,63.67,63.78,64.06,64.24,64.5,64.5,64.99,64.89,65.49,65.28,65.64,65.84,66],\
[20.65,24.2,27.81,30.55,33.64,35.94,37.21,40.13,41.53,43.55,44.83,45.95,47.71,49.19,50.4,52.26,52.97,53.96,54.97,56.07,56.82,58.11,58.97,60.07,60.22,61.62,62.42,63.03,64.13,64.7,65.81,65.92,66.93,67.28,68.26,69.34,69.75,70.58,71.01,71.57,72.22,73.29,73.64,74.57,75,75.32,76,77.06,77.46,78.26,78.89,79.38,79.73,80.7,80.86,81.27,82.1,82.72,83.13,83.71,84.24,84.85]]

influent=[[4.07,4.59,5,5.63,5.87,6.34,6.57,6.91,7.13,7.58,7.55,7.89],\
[12.36,15.46,18.06,20.47,22.87,25.33,26.63,28.66,30.06,31.38,32.95,34.22,35.51,36.57,37.62],\
[23.77,30.08,35.08,38.94,43.21,46.13,48.65,51.59]]

meth=[[38.6,48.65,57.61,65.94,72.17,77.59,82.88,88.43,93.96,96.68,102.26,106.34,109.96,114.1,117.43,120.04,123.62,126.56],\
[40.91,52.23,62.22,70.49,79.1,85.89,93.23,98.07,102.62,108.03,113.23,117.78,121.59,126.52,130.57],\
[45.92,59.18,70.1,79.23,87.67,94.23,100.9,107.58,112.5,117.78,122.66,128.03,132.45,136.93,140.89,145.06,148.56,152.75,155.88,157.88,162.49,165.5,168.16,170.86,174.34,176.88,178.97,182.43,184.58,186.93,189.41,191.49,193.48,196.4,197.78,200.85,202.21,204.47,206.62,208.56,210.07,212.35,213.8,215.65,217.65,219.19]]

ob=[[20.62,24.94,28.37,31.19,33.49,36.44,38.25,40.49,41.96,44.36,45.38,46.92,48.47,49.57,51.05,51.76,53.81,54.61,55.67,57.35,57.45,58.11,59.47,60.46,61.16,61.95,62.55,63.51,63.53,64.82,65.89,66.16,66.91,67.13,68.5,68.47,69.48,70.79,70.31,70.88,71.4,72.51,71.96,73.21,73.61,74.01,74.71,75.3,75.64,76.07,76.7,76.78,77.29,78.11,78.44,78.79,79.5,80.01,79.82,80.36,80.73,81.39,81.79,81.83,82.53,82.91,83.23,83.53,83.62,84.3,84.59,85.06,85.48,85.86,85.97,86.24,86.74,87,87.45,87.73],\
[28.12,35.8,42.69,47.92,53.85,58.74,62.87,67.53,71.4,75.47,78.97,82.52,85.43,89.26,91.75,95.27,97.9,100.41,103.27,105.38,108.9,111.39,113.47],\
[33.99,42.36,48.73,56.44,61.16,66.01,71.23,75.64,80.16,84.11,87.62,92.58,96.05,98.85,102.26,105.72,109.12,112.59,115.04,118.15,120.83,123.64,126.26],\
[40.2,50.48,58.4,65.36,71.29,76.31,81.69,86.42,90.13,94.36,98.18,102.48,105.78,108.28,112.03,114.32,116.34,119.38,122.1,125.37,127.1,129.88,131.8,134.33,136.39,137.76,139.75,141.61,143.68,145.64,147.41,149.01,150.56],\
[30.36,38.78,45.68,52.01,57.52,62.1,65.56,69.28,75.47,76.38,79.17,83.95,87.29,89.83,92.49,94.62,97.53,100.11,102.42,105.16,107.5,109.02,111.64,112.92,114.83,117.33,119.49,120.97,123.22,124.88,126.64,128.92,129.96,131.33,132.74,134.83,135.21,137.58,138.8,140.43,141.64,143.39,145.64,145.34,147.43,148.24,149.85,151.41,151.52,153.02,154.44,155.31,156.35,157.92,158.76,159.84,160.96,161.76,162.94],\
[42.31,52.7,60.78,67.92,74.92,80.21,84.14,90.46,93.96,97.91,101.76,105.73,109.68,113.07,115.89,118.44,121.3,123.61,126.58,130.54,132.77,135.95,138.29,140.52,141.61,145.91,147.42,148.15,151.49,152.89,154.69,156.42,159.18,160.34,162.26,164.09,166.1,167.39,169.66,170.84,172,174.05,175.69,176.68,178.25,179.91,180.97,183.1,184.29,185.47,186.58,188.55,189.41,190.46,192.04],\
[26.26,33.71,40.2,46.01,50.24,56.54,60.08,64.18,67.48,70.8,73.86,78.18,81.35,84.57,87.57,90.1,92.04,95.1,98.03,100.05,102.8,103.14,106.35,108.44,110.2,112.73,114.5,117.62,118.92,120.77,123.02,125.4,125.99,127.54,129.71,130.87,131.99,134.05,135.03,137.24,138.04,139.86,141.86,142.61,143.89,145.89,147.95,148.06,150.5,151.03,152.23,153.84,155.43,156.35,157.48,159.22,160.26,161.05,162.46,163.16,164.06,164.86,166.58,167.99,168.37,169.25,171.5,171.71,173.49,173.85,174.98,175.8,177.61,177.88,178.75,179.33,180.48,181.45,182.29,183.54,184.59,185.11,186.36,187.67,187.91,188.57,189.55,190.31,191.02,191.51,192.79,193.25,194.38,195.23,195.89,196.69]]

out=[[32.82,43.36,49.62,58.32,64,70.71,77.48,81.44,87.57,92.26,96.78,100.91,104.91,109.36,113,116.4,120.44,123.68,127.33,129.78,133.65,136.46],\
[50.58,65.82,78.39,89.27,98.78,107.7,115.75,122.72,129.67,136.62,141.73,146.64,152.72,157.54,162.3,167.18,171.36,175.23],\
[51.85,66.35,80.64,93.57,103.88,113.74,122.08,132.78,139.79,147.26,154.55,161.73,169.41,175.22,182.09,188.01,193.84,199.6,205.38,211.59,214.42,220.38,224.81,229.29,233.47,238.64,242.85,246.42,250.59,254.41,259.38,262.02,266.56,270.45,273.95,277.18,281.58,284.78,287.64,291.32,294.36,297.55,300.34,303.45,306.81,309.47,312.76]]

scp=[[22.05,27.03,32.38,35.89,38.69,42.98,45.47,47.57,49.28,51.79,53.75,56.01,57.1,58.36,59.79,61.26,62.59,64.16,64.73,65.49,67.01,68.04,68.53,69.98,70.76,72.13,73.1,73.53,73.49,75.17,76.16,76.47,76.95,77.62,78.62,78.97,79.04,80.01,80.4,81.92,81.39,82.55,82.51,82.98,83.87,84.17,84.83,84.76,86.09,85.85,86.94,87.09,87.31,87.79,88.53,88.77,88.99,89.49,89.7,90.57,90.91,91.22,91.58,91.87],\
[25.68,31.93,38.04,42.6,48.1,52.83,56.22,59.79,63.86,66.59,69.73,72.77,74.83,77.26,80,82.6,85.08,87.26,89.59,91.87,93.85],\
[27.28,34.13,40.66,45.86,50.39,54.07,58.36,62.19,65.92,68.54,72.4,73.92,77.06,79.86,82.73,85,87.08,89.92,91.65,93.77,95.45,97.58,99.74,101.27,102.67],\
[19.09,23.76,29.82,32.48,36.27,39.42,42.22,46.12,48.31,51.36,53.72,55.07,57.93,60.18,62.21,64.17,65.84,67.35,69.55,71.18,74.39,75.12,75.74,78.16,79.27,79.94,82.17,82.63,84.93,85.43,87.28,89.68,90.12,91.18,92.1,92.7,94.68,95.12,96.5,97.87,98.92,99.74,100.53,101.3,103.15,103.64,104.44,105.46,106.56,107.79,107.84,108.92,109.83,110.62,111.11,112.53,112.82,113.59,114.77,115.66,116.24,116.5,117.92,118.08,119.04,119.74,120.35,121.33,121.9,122.54],\
[28,35.46,41.56,48.32,53.52,58.61,62.62,67.44,70.76,73.77,77.91,81.52,84.89,87.73,91.78,92.81,96.54,98.39,101.24,102.92,106.23,107.38,110.15,113.05,114.87,117.19,118.86,120.72,123.1,124.83,126.55,128.03,129.97,131.88,133.47,134.89,136.47,137.16,139.6,141.03,142.58,144.09,145.13,146.64],\
[37.31,47.24,55.66,63.17,69.22,76.28,81.05,87.08,91.93,96.59,100.73,103.62,108.45,112.07,114.79,118.08,121.91,124.28,127.36,130.66,132.62,135.18,137.75,140.47,142.62,144.35,145.63,148.5,150.83,152.74,154.37,156.29,158.07,159.38,161.11,163.03,164.82,165.9,167.32,168.9,170.47]]

""" Matplotlib Colors
        * b : blue
        * g : green
        * r : red
        * c : cyan
        * m : magenta
        * y : yellow
        * k : black
        * w : white
        
        63aafe - total
        dd2d32 - influent
        fff58c - eqbasin
        6711ff - meth
        00ff00 - aerobic
        fea746 - effluent
        865357 - ob
        00ccff - scp
"""

envcolor = dict({'total':'#63aafe',\
'influent':'#dd2d32',\
'eqbasin':'#fff58c',\
'meth':'#6711ff',\
'aerobic':'#00ff00',\
'effluent':'#fea746',\
'ob':'#865357',\
'scp':'#00ccff'})

print "Graphing..."

#determine which samples to graph and prepare sample related graph information

fig = plt.figure()
ax = fig.add_subplot(111)
alph = 0.15

#aeb
plot_data(ax,xaxis, aeb, envcolor['aerobic'],alph,[0,2])

#eqbasin
plot_data(ax,xaxis, eqbasin, envcolor['eqbasin'],alph+.1,[0,2,3])

#influent
plot_data(ax,xaxis, influent, envcolor['influent'],alph,[0,1,2])

#meth
plot_data(ax,xaxis, meth, envcolor['meth'],alph,[0,2])

#ob
plot_data(ax,xaxis, ob, envcolor['ob'],alph,[0,6,5])

#out
plot_data(ax,xaxis, out, envcolor['effluent'],alph,[0,2])

#scp
plot_data(ax,xaxis, scp, envcolor['scp'],alph,[0,3,4,5])

#for posters
"""
plt.rcParams['font.size'] = 24
plt.xlabel("Number of Sequences", fontsize=24)
plt.ylabel("Number of OTUs", fontsize=24)"""

#for print

plt.rcParams['font.size'] = 12
plt.xlabel("Number of Sequences", fontsize=12)
plt.ylabel("Number of OTUs", fontsize=12)

plt.show()

print "Done!"
