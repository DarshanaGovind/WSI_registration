# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 10:44:45 2019
@author: Darshana Govind (d8@buffalo)
"""

import openslide
import numpy as np
import matplotlib.pyplot as plt
from skimage import transform
import cv2

source=openslide.open_slide("ImageA.svs")
source2 = openslide.open_slide("ImageB.svs")

print("Opening WSIs in mid resolution...")
ImgA = np.array(source2.read_region((0,0),1,source2.level_dimensions[1]),dtype = "uint8")
ImgB = np.array(source.read_region((0,0),1,source.level_dimensions[1]),dtype = "uint8")

print("Removing alpha channel...")
ImgA1 = ImgA[:,:,0:3]
ImgB1 = ImgB[:,:,0:3]

print("Registering images...")

plt.figure()
plt.imshow(ImgB1)
print("Please click 10 points from Image1")
x = plt.ginput(10)
print("clicked", np.asarray(x))
plt.show()

plt.figure()
plt.imshow(ImgA1)
print("Please click 10 points from Image2")
y = plt.ginput(10)
print("clicked", np.asarray(y))
plt.show()

tform = transform.estimate_transform('similarity', np.asarray(x),np.asarray(y))
registered_image = transform.warp(ImgB1, inverse_map=tform.inverse) 

