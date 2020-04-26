import cv2 as cv
import numpy as np
import staffs

TEMPLATE_STAFF_SPACE = 14
BLUR_KERNEL = 3

"""Applies binarization and staff detection to the given image, resizes the image.
    :param: image as a byte array
    :return: resized image, array with staff locations, float that represents the space between staff lines"""


def preprocessed_data(image_bytes):
    decoded = cv.imdecode(np.frombuffer(image_bytes, np.uint8), -1)
    img_gray = cv.cvtColor(decoded, cv.COLOR_BGR2GRAY)

    thres, img_black_and_white = cv.threshold(img_gray, 127, 255, cv.THRESH_BINARY)
    cv.imwrite('../testing/tulemus.png', img_black_and_white)

    staff_lines = staffs.staff_detection(img_gray)
    if len(staff_lines) > 1:
        space_between_staffs = staffs.find_space_between_lines(staff_lines)
        width, height = img_black_and_white.shape
        size_difference = TEMPLATE_STAFF_SPACE / space_between_staffs
        img_sized = cv.resize(img_black_and_white, (int(height * size_difference), int(width * size_difference)))
        return img_sized, staff_lines, space_between_staffs, size_difference

