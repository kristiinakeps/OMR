import cv2 as cv
import numpy as np
import staff

TEMPLATE_STAFF_SPACE = 14
BLUR_KERNEL = 3

"""Applies binarization and staff detection to the given image, resizes the image.
    arguments: image as a byte array
    returns: resized image, array with staff locations, float that represents the space between staff lines"""
def preprocessed_data(image_bytes):
    decoded = cv.imdecode(np.frombuffer(image_bytes, np.uint8), -1)
    img_gray = cv.cvtColor(decoded, cv.COLOR_BGR2GRAY)

    thres, img_black_and_white = cv.threshold(img_gray, 127, 255, cv.THRESH_BINARY)
    cv.imwrite('../testing/tulemus.png', img_black_and_white)

    staffs = staff.staff_detection(img_gray)
    if len(staffs) > 1:
        space_between_staffs = staff.find_space_between_lines(staffs)
        width, height = img_black_and_white.shape
        size_difference = TEMPLATE_STAFF_SPACE / space_between_staffs
        img_sized = cv.resize(img_black_and_white, (int(height * size_difference), int(width * size_difference)))
        return img_sized, staffs, space_between_staffs, size_difference



if __name__ == "__main__":
    # with open("../testing/camera.jpg", "rb") as f:
    # with open("../testing/mary_lamb.png", "rb") as f:
    # with open("../testing/test.png", "rb") as f:
    with open("../testing/test_rythm.png", "rb") as f:
    # with open("../testing/high.png", "rb") as f:
        image_bytes = f.read()
    res = preprocessed_data(image_bytes)
    if res is not None:
        result, staffs, space, size_difference = res
        coordinates_and_notes, rows = staff.group_and_identify(staffs, space, size_difference)
        # co_list = sorted(list(coordinates_and_notes.items()), key=lambda x: x[0])
        # print(co_list)
        # print(rows)

        import recognition2
        locs = recognition2.recognize_all_symbols(result, coordinates_and_notes, rows)
        print(locs)

    # if result is not None:
    #     cv.imwrite('../testing/tulemus2.png', result)

    # decoded = cv.imdecode(np.frombuffer(image_bytes, np.uint8), -1)
    # decoded = cv.rotate(decoded, cv.ROTATE_180)
    # cv.imwrite('../testing/tulemus2.png', result)

