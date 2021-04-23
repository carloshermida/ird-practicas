#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module to plot images over geographical data, based on coordinates.
"""

import shapefile as shp
import matplotlib.pyplot as plt
import seaborn as sns
from pyproj import Proj
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import os

def plotMap(points=[], x_lim = None, y_lim = None, figsize = (9,7), 
            shp_path="recursos"+os.sep+"Concellos"+os.sep+"Concellos_IGN",
            img_path="recursos"+os.sep+"weatherIcons"+os.sep):
    '''
    Plot map with lim coordinates and images in the designated points.
    '''
    sns.set(style="whitegrid", palette="pastel", color_codes=True)
    sns.mpl.rc("figure", figsize=(9,7))

    print(shp_path)
    print(os.path.abspath(shp_path))
    sf = shp.Reader(shp_path)

    print("Shape size: "+str(len(sf)))
    print("Shaperecords size: "+str(len(sf.shapeRecords())))
    print("Points size: "+str(len(points)))	
    
    fig, ax = plt.subplots(figsize=figsize)

    for shape in sf.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]

        ax.plot(x, y, 'k', color="grey")

    if (x_lim != None) & (y_lim != None):     
        ax.xlim(x_lim)
        ax.ylim(y_lim)

    # Convert coordinates to UTM projection
    myProj = Proj("+proj=utm +zone=29K, +ellps=WGS84 +datum=WGS84 +units=m +no_defs")

    # Show selected image in the designated coordinates
    for p in points:
        UTMx, UTMy = myProj(p[1][0], p[1][1])

        print(str(UTMx) + " - " + str(UTMy))
        
        img_file = img_path+"default.png"
        if os.path.exists(img_path+str(p[0])+".png"):
            img_file = img_path+str(p[0])+".png"
        else:
            print("Not found: "+img_path+str(p[0])+".png")

        ab = AnnotationBbox(OffsetImage(plt.imread(img_file)), (UTMx, UTMy), frameon=False)
        ax.add_artist(ab)
    fig.savefig("mapa.png")    

