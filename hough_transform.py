import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from skimage.transform import rotate
from skimage.transform import (hough_line, hough_line_peaks, resize)
from scipy.stats import mode
from skimage import io
import cv2 as cv
from skimage.filters import threshold_otsu, sobel


def binarizeImage(RGB_image):

    image = rgb2gray(RGB_image)
    threshold = threshold_otsu(image)
    bina_image = image < threshold

    return bina_image


def findEdges(bina_image):

    image_edges = sobel(bina_image)

    # plt.imshow(bina_image, cmap='gray')
    # plt.axis('off')
    # plt.title('Binary Image Edges')

    return image_edges


def findTiltAngle(image_edges):

    h, theta, d = hough_line(image_edges)
    accum, angles, dists = hough_line_peaks(h, theta, d)
    angle = np.rad2deg(mode(angles, keepdims=True)[0][0])

    if (angle < 0):
        return angle + 90
    else:
        return angle - 90


def rotateImage(RGB_image, angle):
    height, width, depth = RGB_image.shape
    max_size = width
    if height > width:
        add_more = int((height - width)/2)
        resized_img = cv.copyMakeBorder(RGB_image, 0, 0, add_more, add_more,
                                        cv.BORDER_CONSTANT, None, value=0)
    else:
        add_more = int((width - height)/2)
        resized_img = cv.copyMakeBorder(RGB_image, add_more, add_more, 0, 0,
                                        cv.BORDER_CONSTANT, None, value=0)

    fixed_image = rotate(resized_img, angle)

    return fixed_image


def generalPipeline(img, is_save=False):
    image = io.imread(img)
    try:
        bina_image = binarizeImage(image)
        image_edges = findEdges(bina_image)
        angle = findTiltAngle(image_edges)
        fixed_image = rotateImage(image, angle)
        # =============================================================================
        if is_save:
            io.imsave(img, (fixed_image*255).astype(np.uint8))
        else:
            plt.imshow(fixed_image)
            plt.axis('off')
            plt.title('Fixed Image')
            plt.show()
        # =============================================================================
        return fixed_image, img
    except:
        print('error')
        return image, img


if __name__ == "__main__":
    img_ptah_3 = './images/meter_for_test_3.jpeg'
    generalPipeline(img_ptah_3, False)
    img_ptah_4 = './images/meter_for_test_4.jpeg'
    generalPipeline(img_ptah_4, False)
    img_ptah_5 = './images/meter_for_test_5.jpeg'
    generalPipeline(img_ptah_5, False)
    # img_ptah_5 = './run_meter/1677607918/crops/model 1/img1.jpg'
    # generalPipeline(img_ptah_5, False)
