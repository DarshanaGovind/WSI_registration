# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 14:13:52 2021

@author: Darshana Govind (d8@buffalo.edu)

"""

import sys
sys.path.append("./functions/")
import warnings
import numpy as np
import openslide
from skimage.transform import rescale 
from getMaskFromXml import getMaskFromXml
from skimage.measure import label,regionprops
import cv2
import matplotlib.pyplot as plt
from skimage.transform import warp
from skimage.transform import SimilarityTransform
from getWindows import getWindows
from skimage.transform import resize

warnings.filterwarnings("ignore")



'''User inputs'''
'''==========='''

highres_w = 200   
sourcePAS = openslide.open_slide("/hdd/d8/tempslides/PAS/JW1.svs")
sourceIF = openslide.open_slide("/hdd/d8/tempslides/IF/JW1.svs")
PASxmlpath = "/hdd/d8/tempslides/PAS/JW1.xml" #glom annotation path


'''Read images in mid resolution'''
'''=============================='''
print("Opening WSIs in mid resolution...")
PAS = np.array(sourcePAS.read_region((0,0),1,sourcePAS.level_dimensions[1]),dtype = "uint8")
IF = np.array(sourceIF.read_region((0,0),1,sourceIF.level_dimensions[1]),dtype = "uint8")



'''Get MPP and scaling'''
'''===================================='''
print("Rescaling PAS...")
PAS_mpp = (float(sourcePAS.properties[openslide.PROPERTY_NAME_MPP_X])+float(sourcePAS.properties[openslide.PROPERTY_NAME_MPP_Y]))/2
IF_mpp = (float(sourceIF.properties[openslide.PROPERTY_NAME_MPP_X])+float(sourceIF.properties[openslide.PROPERTY_NAME_MPP_Y]))/2
Pas_downscale_value = PAS_mpp/IF_mpp

if PAS_mpp ==IF_mpp:
    PAS_rescaled = PAS
else:
    PAS_rescaled = rescale(PAS, Pas_downscale_value, anti_aliasing=False)


     
'''Register slides'''
'''===================================='''
print("Registering...")

chktform = SimilarityTransform(scale=None, rotation=None, translation=(1,162))
FinalregIF = warp(IF[:,:,0:3], inverse_map=chktform.inverse,output_shape=PAS_rescaled[:,:,0:3].shape)

'''XML annotation to mask'''
'''===================================='''  

PASmask = rescale(getMaskFromXml(sourcePAS,PASxmlpath), Pas_downscale_value, anti_aliasing=False)
  
'''Extract each glom as per H-AI-L annotations'''
'''===================================='''  

countPatch  = 0 
PAS_podmask = np.zeros(PAS_rescaled[:,:,0].shape)

c = 0
for region in regionprops(label(PASmask)):
    c +=1
    minr, minc, maxr, maxc = region.bbox
    GlomArea = region.area
    
    ptx = (minr+maxr)/2
    pty = (minc+maxc)/2            
    
    
    crop_imgIF,crop_imgPAS = getWindows(sourcePAS,sourceIF,pty,ptx,chktform,highres_w) # Extract high resolution ROIs
    Glommask2 = resize((PASmask[ptx-(highres_w/2):ptx+(highres_w/2),pty-(highres_w/2):pty+(highres_w/2)]), ((highres_w*4,highres_w*4)),anti_aliasing=True)
    Glommask2 = cv2.threshold((Glommask2), 0.1, 255, cv2.THRESH_BINARY)[1]

    plt.figure()
    plt.subplot(131)
    plt.gca().set_title('PAS')
    plt.imshow(crop_imgPAS[:,:,0:3])
    plt.subplot(132)
    plt.gca().set_title('IHC')
    plt.imshow(crop_imgIF[:,:,0:3])
    plt.subplot(133)
    plt.gca().set_title('Overlay')
    plt.imshow(crop_imgPAS[:,:,0:3])
    plt.imshow(crop_imgIF[:,:,0:3],alpha = 0.5)
    plt.show()  
