__author__ = "Shishir Shah"
__version__ = "1.0.0"
__copyright__ = "Copyright 2022 by Shishir Shah, Quantitative Imaging Laboratory (QIL), Department of Computer  \
                Science, University of Houston.  All rights reserved.  This software is property of the QIL, and  \
                should not be distributed, reproduced, or shared online, without the permission of the author."

import numpy as np
import copy
from dpcourse import Stack
from dpcourse import Queue


class MyImage:
    ''' Already defined is the constructor that initializes the values for the
    data items necessary to represent an image.'''
    def __init__(self):
        '''This is the n-d array that stores the image intensity values.'''
        self.data = None
        '''This defines the size of the image as [width, height].'''
        self.size = [0, 0]
        '''This defines the number of image channels and should be 1 for gray scale and 3 for color image.'''
        self.channels = None
        '''This defined the maximum intensity values.  
        In our case, since we will restrict to 8-bit images, this will be 255.'''
        self.bitdepth = None
        '''This specifies if the image is PGM or PPM, hence would take values of 'P2' or 'P3', respectively.'''
        self.category = None

    ''' Write the method to read either a PGM or PPM files given the filename as the argument.  
    All the defined data attributes in the constructor should have appropriate values after reading the file.'''
    def load_image(self, filename):
        values = []
        with open(filename, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                elif line.startswith('#'):
                    pass
                else:
                    temp = line.split()
                    for i in range(len(temp)):
                        values.append(temp[i])

        self.category = values[0]
        self.size = [int(values[1]), int(values[2])]
        self.bitdepth = values[3]
        nvals = list(map(int, values[4:]))
        if self.category == 'P2':
            self.channels = 1
        elif self.category == 'P3':
            self.channels = 3
        else:
            print('File type not supported\n')
            return
        self.data = np.reshape(nvals, (self.size[1], self.size[0], self.channels))
        return

    ''' Write the method to save either a PGM or PPM files given the filename as the argument.'''
    def save_image(self, filename):
        if self.category == None:
            print('Image does not exist so cannot be saved\n')
        else:
            fp = open(filename, 'w')
            fp.write(self.category + '\n')
            img_size = str(self.get_width()) + ' ' + str(self.get_height())
            fp.write(img_size + '\n')
            fp.write(str(self.bitdepth) + '\n')
            for x in self.data:
                for y in x:
                    fp.write(" ".join(map(str, y)))
                    fp.write('\n')
            fp.close()
        return

    ''' Write the method to create a new image of dimension 'width' by 'height' and 
    with all pixels having intensity values provided by the argument 'value'.'''
    def new_image(self, width, height, value):
        self.size = [width, height]
        self.channels = len(value)
        self.bitdepth = 255
        if self.channels == 1:
            self.data = np.zeros([height, width, 1], dtype=np.uint8)
            self.category = 'P2'
        elif self.channels == 3:
            self.data = np.zeros([height, width, 3], dtype=np.uint8)
            self.category = 'P3'
        self.data[:, :] = value

    ''' Write method that returns the number of channels an image has.  
    Recall that this value is 1 for gray scale images and 3 for color images.'''
    def get_channels(self):
        return self.channels

    ''' Write method that returns the n-d array having the intensity values of the image.'''
    def get_image_data(self):
        return self.data

    ''' Write method that return the width of the image.'''
    def get_width(self):
        return self.size[0]

    ''' Write method that return the height of the image.'''
    def get_height(self):
        return self.size[1]

    '''' Write method that assigns intensity value of a range of image pixels to 
    that given by the argument 'value' where the range of pixel locations is specified 
    as a bounding box in the format [x, y, width, height].'''
    def set_image_pixels(self, bbox, value):
        startx = bbox[0]
        starty = bbox[1]
        endx = startx + bbox[2]
        endy = starty + bbox[3]
        self.data[starty:endy, startx:endx] = value
        return

    '''' Write method that return an n-d array of intensity values for a range of image pixels
    where the range is specified as a bounding box in the format [x, y, width, height].'''
    def get_image_pixels(self, bbox):
        startx = bbox[0]
        starty = bbox[1]
        endx = startx + bbox[2]
        endy = starty + bbox[3]
        return self.data[starty:endy, startx:endx]

    ''' Write a method that assigns the pixel value in the image at 
    location 'x', 'y' to the intensity given by argument 'value'.'''
    def set_image_pixel(self, x, y, value):
        self.data[y, x] = value
        return

    ''' Write a method that returns the pixel value in the image at 
    location 'x', 'y'.'''
    def get_image_pixel(self, x, y):
        return self.data[y, x]

    ''' Write method that converts a color image to a gray scale image 
    by computing the average of the red, green, and blue intensity value 
    at each pixel of the color image.  Please note that this should only 
    happen if the image is a color image.'''
    def color_to_gray(self):
        if self.channels == 1:
            print('Image is already gray scale\n')
        else:
            self.channels = 1
            self.category = 'P2'
            grayvals = []
            for x in self.data:
                for y in x:
                    gray = 0
                    for z in y:
                        gray += z
                    gray = int(gray / 3)
                    grayvals.append(gray)
            self.data = np.reshape(grayvals, (self.size[1], self.size[0], self.channels))
        return

    ''' Write method to threshold a gray scale image based on value of argument 'N'.'''
    def threshold_gray(self, N):
        if self.channels == 3:
            print('Image is color.  Please convert to gray level before thresholding.\n')
        else:
            self.channels = 1
            self.category = 'P2'
            newvals = []
            for x in self.data:
                for y in x:
                    if y <= N:
                        newvals.append(0)
                    else:
                        newvals.append(255)
            self.data = np.reshape(newvals, (self.size[1], self.size[0], self.channels))
        return