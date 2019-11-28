# Reference:
# https://github.com/getsanjeev/compression-DCT
# https://www.sciencedirect.com/topics/computer-science/quantization-matrix

import cv2
import numpy as np
import math
from compressType import CompressType

# import zigzag functions
from zigzag import *

class RLE2Image:
    def __call__(self, comp_type, enc_txt, out_img):
        # Quantization Matrix
        if comp_type is CompressType.CHROME:
            # Standard JPEG Quality Factor for **Chrominance**
            QUANTIZATION_MAT = np.array([17,18,24,47,99,99,99,99],[18,21,26,66,99,99,99,99],[24,26,56,99,99,99,99,99],[47,66,99,99,99,99,99,99],[99,99,99,99,99,99,99,99],[99,99,99,99,99,99,99,99],[99,99,99,99,99,99,99,99],[99,99,99,99,99,99,99,99])
        else:   # Default: LUM
            # Standard JPEG Quality Factor for **Luminance**
            QUANTIZATION_MAT = np.array([[16,11,10,16,24,40,51,61],[12,12,14,19,26,58,60,55],[14,13,16,24,40,57,69,56 ],[14,17,22,29,51,87,80,62],[18,22,37,56,68,109,103,77],[24,35,55,64,81,104,113,92],[49,64,78,87,103,121,120,101],[72,92,95,98,112,100,103,99]])
        
        # defining block size
        block_size = 8

        # Reading enc_txt to decode it as image
        with open(enc_txt, 'r') as myfile:
            image=myfile.read()

        # spplits into tokens seperated by space characters
        details = image.split()

        # just python-crap to get integer from tokens : h and w are height and width of image (first two items)
        h = int(''.join(filter(str.isdigit, details[0])))
        w = int(''.join(filter(str.isdigit, details[1])))

        # declare an array of zeros (It helps to reconstruct bigger array on which IDCT and all has to be applied)
        array = np.zeros(h*w).astype(int)


        # some loop var initialisation
        k = 0
        i = 2
        x = 0
        j = 0


        # This loop gives us reconstructed array of size of image

        while k < array.shape[0]:
        # Oh! image has ended
            if(details[i] == ';'):
                break
        # This is imp! note that to get negative numbers in array check for - sign in string
            if "-" not in details[i]:
                array[k] = int(''.join(filter(str.isdigit, details[i])))        
            else:
                array[k] = -1*int(''.join(filter(str.isdigit, details[i])))        

            if(i+3 < len(details)):
                j = int(''.join(filter(str.isdigit, details[i+3])))

            if j == 0:
                k = k + 1
            else:                
                k = k + j + 1        

            i = i + 2

        array = np.reshape(array,(h,w))

        # loop for constructing intensity matrix form frequency matrix (IDCT and all)
        i = 0
        j = 0
        k = 0

        # initialisation of compressed image
        padded_img = np.zeros((h,w))

        while i < h:
            j = 0
            while j < w:        
                temp_stream = array[i:i+8,j:j+8]                
                block = inverse_zigzag(temp_stream.flatten(), int(block_size),int(block_size))            
                de_quantized = np.multiply(block,QUANTIZATION_MAT)                
                padded_img[i:i+8,j:j+8] = cv2.idct(de_quantized)        
                j = j + 8        
            i = i + 8

        # clamping to  8-bit max-min values
        padded_img[padded_img > 255] = 255
        padded_img[padded_img < 0] = 0

        # compressed image is written into out_img file
        cv2.imwrite(out_img,np.uint8(padded_img))

        # DONE!