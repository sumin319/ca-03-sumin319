__author__ = "Shishir Shah"
__version__ = "1.0.0"
__copyright__ = "Copyright 2022 by Shishir Shah, Quantitative Imaging Laboratory (QIL), Department of Computer  \
                Science, University of Houston.  All rights reserved.  This software is property of the QIL, and  \
                should not be distributed, reproduced, or shared online, without the permission of the author."


import sys
from imageops.DSImage import MyImage as MyImage
from dpcourse import Stack
from dpcourse import Queue
from dpcourse import LinkedList
import random
import math


class Blob:

    ''' Already defined is the constructor that initializes
    the attributes to be maintained to an identified binary
    labeled object (region) in an image.'''
    def __init__(self):
        '''This is the linked list to store all pixel positions belonging to the blob (region).'''
        self.region = LinkedList.LinkedList()
        '''This is the color assigned to be blob (region) during connected component analysis.'''
        self.color = [0, 0, 0]
        '''This is the centroid specified as x and y image coordinate for the blob (region).'''
        self.centroid_x = 0
        self.centroid_y = 0
        '''This is the total number of pixels that belong to the blob (region), 
        also considered as the area of the blob.'''
        self.size = 0
        '''This is the bounding box coordinates for the blob specified
        as [min_x, min_y, max_x, max_y].'''
        self.bbox = []
        '''This is the id or a count given to the blob considering that each blob is unique.'''
        self.id = 0



    '''Write a method that adds the pixel location given 
    as 'x_pos' and 'y_pos' to the linked list that maintains 
    a list of pixels belonging to a particular region.'''
    def add(self, x_pos, y_pos):
        self.region.add((x_pos, y_pos))
        self.size += 1
        self.set_bbox()
        self.centroid_x = (self.bbox[0] + self.bbox[2]) / 2
        self.centroid_y = (self.bbox[1] + self.bbox[3]) / 2

    '''Write a method to set the id for the blob (region) 
    given the input argument 'num'.'''
    def set_id(self, num):
        self.id = num

    '''Write a method to get the id for the blob (region).'''
    def get_id(self):
        return self.id

    '''Write a method to set the color for the blob (region) 
    such that it can be used to generate a blob image.'''
    def set_color(self, color):
        self.color = color

    '''Write a method to get the color for the blob (region) 
    such that it can be used to generate a blob image.'''
    def get_color(self):
        return self.color

    '''Write a method to return the centroid of the blob (region).'''
    def get_centroid(self):
        return [self.centroid_x, self.centroid_y]

    '''Write a method to return the size (area) of the blob (region).'''
    def get_size(self):
        return self.size

    '''Write a method to set the bounding box of the blob (region).
    The bounding box should be specified as the upper left coordinates (min_x, min_y)
    and the lower right coordinates (max_x, max_y) that surrounds the blob (region).'''
    def set_bbox(self):
        current = self.region.head
        bbox = [current.get_data()[0], current.get_data()[1],
                current.get_data()[0], current.get_data()[1]]
        while current != None:
            if bbox[2] < current.get_data()[0]:
                current.get_data()[0] = bbox[2]
            if bbox[3] < current.get_data()[1]:
                current.get_data()[1] = bbox[3]
            if bbox[0] > current.get_data()[0]:
                current.get_data()[0] = bbox[0]
            if bbox[1] > current.get_data()[1]:
                current.get_data()[1] = bbox[1]
            current = current.get_next()
        self.bbox = bbox

    '''Write method to return the bounding box of the blob (region).'''
    def get_bbox(self):
        return self.bbox


class RegionAnalysis:

    def __init__(self, image):
        try:
            if not isinstance(image,MyImage):
                raise TypeError
        except TypeError:
            print('Image has to be type MyImage.')
            sys.exit(2)
        try:
            if image.get_channels() != 1:
                raise TypeError
        except TypeError:
            print("Image has to be binary image.")
            sys.exit(2)
        self.binary_image = image
        self.height = image.get_height()
        self.width = image.get_width()
        self.label_image = MyImage()
        self.label_image.new_image(self.width, self.height, [0, 0, 0])
        self.num_regions = 0

        '''The following attributes enhance the class implemented in CA-02.'''

        '''This is the linked list of all blobs (regions) in the image after 
        completing connected component analysis.'''
        self.regions = LinkedList.LinkedList()
        '''This is the blob image that would show blobs (regions) of interest.'''
        self.blob_image = MyImage()
        '''This is the initiated blob image, with all pixels being black.'''
        self.blob_image.new_image(self.width, self.height, [0, 0, 0])
        '''This is the total number of blobs (regions) of interest.'''
        self.num_blobs = 0

    '''This method generates a random trichromat value as a list to be used
    in assigning a color value.'''
    def __generate_random_labelvalue(self):
        a = random.randint(1, 255)
        b = random.randint(1, 255)
        c = random.randint(1, 255)
        return [a, b, c]

    '''This method returns the binary image generated as a 
    result of the thresholding operation.'''
    def get_binary_image(self):
        return self.binary_image

    '''This method returns the image with all identified regions such that
    each groups of pixels identified as belong to a region are assigned the 
    same color value.'''
    def get_label_image(self):
        return self.label_image

    '''This method returns the total number of regions resulting from connected
    component analysis.'''
    def get_num_regions(self):
        return self.num_regions

    '''This method performs connected component analysis on the binary image
    using the Stack data structure. This method will need to be modified to accept
    the return value from the modified floodfill method and to add generated blob (region)
    to the linked list that stores all blobs (self.regions).'''

    def connected_components_stack(self):
        data = self.binary_image.get_image_data().copy()
        self.num_regions = 0
        blob = Blob()
        blob.set_id(self.num_regions)
        for i in range(self.width):
            for j in range(self.height):
                if int(data[j, i]) == 255:
                     self.num_regions += 1
                     self.__floodfill_stack(data, i, j)
        self.num_blobs += 1
        self.regions.add(blob)
        return

    '''This method performs connected component analysis on the binary image
    using the Queue data structure. This method will need to be modified to accept
    the return value from the modified floodfill method and to add generated blob (region)
    to the linked list that stores all blobs (self.regions).'''

    def connected_components_queue(self):
        data = self.binary_image.get_image_data().copy()
        self.num_regions = 0

        blob = Blob()
        blob.set_id(self.num_regions)
          for i in range(self.width):
            for j in range(self.height):
                if int(data[j, i]) == 255:
                    self.num_regions += 1
                    self.__floodfill_queue(data, i, j)
          self.num_blobs + 1
          self.regions.add(blob)
          return

    '''This is a private method that performs the floodfill algorithm using
    the Stack data structure.  You may need to modify this method to manage
    each identified blob (region) using the given Blob class and the 
    enhanced RegionAnalysis class. This private method should return a blob (region).'''

    def __floodfill_stack(self, temp, x, y, blob):
            ny = [-1, -1, -1, 0, 0, 1, 1, 1]
            nx = [-1, 0, 1, -1, 1, -1, 0, 1]

            frontier = Stack.Stack()

            pixel_value = int(temp[y, x])
            # target color is same as replacement
            if pixel_value != 255:
                return

            frontier.push([x, y])
            label_value = self.__generate_random_labelvalue()
    self.label_image.set_image_pixel(x, y, label_value)
    temp[y, x] = 0
            while not frontier.is_empty():
                loc = frontier.pop()
                x = loc[0]
                y = loc[1]
                blob.add((x, y))
                for k in range(len(ny)):
                    # if the adjacent pixel at position (x + nx[k], y + ny[k]) is
                    # is valid and has the same color as the current pixel
            if 0 <= y + ny[k] < self.height and 0 <= x + nx[k] < self.width:
            if int(temp[y + ny[k], x + nx[k]]) == pixel_value:
                    frontier.push([x + nx[k], y + ny[k]])
                    self.label_image.set_image_pixel(x + nx[k], y + ny[k], label_value)
                    temp[y + ny[k], x + nx[k]] = 0
    return

    '''This is a private method that performs the floodfill algorithm using
    the Queue data structure. You may need to modify this method to manage
    each identified blob (region) using the given Blob class and the 
    enhanced RegionAnalysis class.  This private method should return a blob (region).'''
    def floodfill_queue(self, temp, x, y):
        ny = [-1, -1, -1, 0, 0, 1, 1, 1]
        nx = [-1, 0, 1, -1, 1, -1, 0, 1]

        # create a queue and enqueue starting pixel
        q = Queue.Queue()
        # get the target color
        pixel_value = int(temp[y, x])

        # target color is same as replacement
        if pixel_value != 255:
            return

        q.enqueue([x, y])
        label_value = self.generate_random_labelvalue()
        self.label_image.set_image_pixel(x, y, label_value)
        temp[y, x] = 0

        # break when the queue becomes empty
        while not q.is_empty():
            # dequeue front node and process it
            loc = q.dequeue()
            x = loc[0]
            y = loc[1]
            blob.add((x,y))
            # process all eight adjacent pixels of the current pixel and
            # enqueue each valid pixel
            for k in range(len(ny)):
                # if the adjacent pixel at position (x + nx[k], y + ny[k]) is
                # is valid and has the same color as the current pixel
                if 0 <= y + ny[k] < self.height and 0 <= x + nx[k] < self.width:
                    if int(temp[y + ny[k], x + nx[k]]) == pixel_value:
                        q.enqueue([x + nx[k], y + ny[k]])
                        self.label_image.set_image_pixel(x + nx[k], y + ny[k], label_value)
                        temp[y + ny[k], x + nx[k]] = 0
        return

    '''Write the method that performs the selection of subset of blobs (regions) from
    all the regions identified after connected component analysis and generates the
    blob image to include those blobs (region) along with a bounding box surrounding
    each of the blobs (regions).'''
    def set_blob_image(self, size_threshold=0):
        current = self.regions.head
        while current != None:
            if blob.size < size_threshold:
                for x in range(blob[2], blob[0]):
                    for y in range(blob[3], blob[1]:
                        self.binary_image[i][j] = 0
            else:
             for x in range(blob[2], blob[0]):
               self.binary_image[i][bbox[3]] = 0
               self.binary_image[i][bbox[1]] =
             for y in range(blob[3], blob[1]):
               self.binary_image[bbox[0]][j] = 0
               self.binary_image[bbox[2]][j] = 0
        current = current.get_next()

    '''Write the method that returns the blob image.'''
    def get_blob_image(self):
        return self.blob_image

    '''Write the method that returns the total number of blobs (regions) 
    resulting from the selection/filtering operation specified to be performed.'''
    def get_num_blobs(self):
        return self.num_blobs
