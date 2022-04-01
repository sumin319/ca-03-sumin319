"""ca_03.py: Starter file to run homework 3"""

__author__ = "Shishir Shah"
__version__ = "1.0.0"
__copyright__ = "Copyright 2022 by Shishir Shah, Quantitative Imaging Laboratory (QIL), Department of Computer  \
                Science, University of Houston.  All rights reserved.  This software is property of the QIL, and  \
                should not be distributed, reproduced, or shared online, without the permission of the author."


import sys
import matplotlib.pyplot as plt
from imageops import DSImage as DSImage
from imageops import RegionAnalysis as RegionAnalysis
import logging
import time


def image_display(image):
    if image.get_channels() == 3:
        plt.imshow(image.get_image_data())
        plt.axis('off')
        plt.show()
    else:
        plt.imshow(image.get_image_data(), cmap='gray', vmin=0, vmax=255)
        plt.axis('off')
        plt.show()
    return


def main():
    """ The main function that parses input arguments, calls the appropriate
     method and writes the output image"""

    # Initialize logging
    Log_Format = "%(levelname)s %(asctime)s - %(message)s"

    logging.basicConfig(filename="output/logfile.log",
                        filemode="w",
                        format=Log_Format,
                        level=logging.INFO)
    logger = logging.getLogger()
    # handler = logging.FileHandler('output/logfile.log')
    # logger.addHandler(handler)
    logger.info('Logging initialized.')

    # Parse input arguments
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument("-i", "--image", dest="image",
                        help="specify the name of the input image", metavar="IMAGE")

    parser.add_argument("-t", "--threshold", dest="threshold",
                        help="specify the value to use for thresholding", metavar="THRESHOLD")

    parser.add_argument("-b", "--blob_size_threshold", dest="blob_size_threshold",
                        help="specify the value to use for thresholding blob size", metavar="BLOBTHRESHOLD")

    parser.add_argument("-m", "--method", dest="method",
                        help="specify the use of Stack or Queue for connected component analysis", metavar="METHOD")

    parser.add_argument("-d", "--display", dest="display",
                        help="specify if images should be displayed", metavar="DISPLAY")

    args = parser.parse_args()

    # Load image
    if args.image is None:
        print("Please specify the name of image")
        print("use the -h option to see usage information")
        logger.error('Input file name not specified.')
        sys.exit(2)
    if args.threshold is None or int(args.threshold) > 255 or int(args.threshold) < 0:
        print("Please specify a usable threshold value")
        print("use the -h option to see usage information")
        logger.error('Threshold value not correctly specified.')
        sys.exit(2)
    if args.blob_size_threshold is None or int(args.blob_size_threshold) < 0 :
        print("Please specify a usable blob size threshold value")
        print("use the -h option to see usage information")
        logger.error('Blob size threshold value not correctly specified.')
        sys.exit(2)
    if args.method is None:
        print("Please specify the use of Stack or Queue for connected component analysis")
        print("use the -h option to see usage information")
        logger.error('Method not specified.')
        sys.exit(2)
    if args.display is None or int(args.display) > 1:
        print("Please specify if images should be displayed or now")
        print("use the -h option to see usage information")
        logger.error('Image display option not correctly specified.')
        sys.exit(2)
    else:
        display = int(args.display)
        thresh = int(args.threshold)
        blob_size = int(args.blob_size_threshold)
        outputDir = 'output/'
        # Initialize image of type MyImage
        myimage = DSImage.MyImage()
        # Load Image specified in input argument
        try:
            myimage.load_image(args.image)
            logger.info('Image loading succeeded.')
        except:
            logger.error('Error loading image.')
        if display == 1:
            image_display(myimage)

        # Convert image to gray level
        try:
            if myimage.get_channels() == 3:
                myimage.color_to_gray()
                if myimage.get_channels() == 1:
                    logger.info('Conversion of color to gray scale image succeeded.')
                    if display == 1:
                        image_display(myimage)
                    output_image_name = outputDir + 'gray_image' + ".pgm"
                    myimage.save_image(output_image_name)
                else:
                    raise ValueError
        except:
            logger.error('Error in converting color image to gray scale image.')

        # Threshold image
        try:
            val = int(myimage.get_image_pixel(myimage.get_width() // 2, myimage.get_height() // 2))
            myimage.threshold_gray(thresh)
            tval = int(myimage.get_image_pixel(myimage.get_width() // 2, myimage.get_height() // 2))
            if val > thresh:
                eval = 255
            else:
                eval = 0
            if tval == eval:
                logger.info('Image thresholding succeeded.')
            else:
                raise ValueError
        except:
            logger.error('Error in thresholding image.')
        if display == 1:
            image_display(myimage)
        output_image_name = outputDir + 'binary_image' + ".pgm"
        myimage.save_image(output_image_name)

        blobs = RegionAnalysis.RegionAnalysis(myimage)
        if args.method == 'Stack':
            blobs.connected_components_stack()
            log_string = 'Total number of regions after connected component analysis using a Stack = ' + str(blobs.get_num_regions())
            print(log_string)
            logger.info(log_string)
            blobs.set_blob_image(blob_size)
            log_string = 'Total number of blobs after filtering using size threshold of ' + str(blob_size) + ' = ' + str(blobs.get_num_blobs())
            print(log_string)
            logger.info(log_string)
        if args.method == 'Queue':
            blobs.connected_components_queue()
            log_string = 'Total number of regions after connected component analysis using a Queue = ' + str(blobs.get_num_regions())
            print(log_string)
            logger.info(log_string)
            blobs.set_blob_image(blob_size)
            log_string = 'Total number of blobs after filtering using size threshold of ' + str(blob_size) + ' = ' + str(blobs.get_num_blobs())
            print(log_string)
            logger.info(log_string)
        if display == 1:
            image_display(blobs.get_label_image())
        output_image_name = outputDir + 'label_image' + ".ppm"
        blobs.get_label_image().save_image(output_image_name)
        output_image_name = outputDir + 'blob_image' + ".ppm"
        try:
            if blobs.get_blob_image() is not None:
                blobs.get_blob_image().save_image(output_image_name)
                log_string = 'Blob image generating and saving successful.'
                print(log_string)
                logger.info(log_string)
                if display == 1:
                    image_display(blobs.get_blob_image())
            else:
                raise AttributeError
        except:
            log_string = 'Error in creating blob image'
            print(log_string)
            logger.error('Error in creating blob image.')


if __name__ == "__main__":
    main()
