import cv2 as cv
import numpy as np
import staff

TEMPLATE_STAFF_SPACE = 14
BLUR_KERNEL = 3

def preprocessed_data(image_bytes):
    decoded = cv.imdecode(np.frombuffer(image_bytes, np.uint8), -1)
    img_gray = cv.cvtColor(decoded, cv.COLOR_BGR2GRAY)

    # img_blur = cv.GaussianBlur(img_gray, (BLUR_KERNEL, BLUR_KERNEL), 0)
    img_blur = img_gray

    thres, img_black_and_white = cv.threshold(img_blur, 127, 255, cv.THRESH_BINARY)
    cv.imwrite('../testing/tulemus.png', img_black_and_white)

    staffs = staff.staff_detection(img_gray)
    if len(staffs) > 1:
        space_between_staffs = staff.find_space_between_lines(staffs)
        print(space_between_staffs)  # mallidel 14, vastavalt sellele tleb pildi suurust muuta
        width, height = img_black_and_white.shape
        size_difference = TEMPLATE_STAFF_SPACE / space_between_staffs
        img_sized = cv.resize(img_black_and_white, (int(height * size_difference), int(width * size_difference)))
        return img_sized, staffs, space_between_staffs
    print(staffs)



if __name__ == "__main__":
    with open("../testing/camera.jpg", "rb") as f:
        image_bytes = f.read()
    result, staffs, space = preprocessed_data(image_bytes)
    if result is not None:
        cv.imwrite('../testing/tulemus2.png', result)
    # decoded = cv.imdecode(np.frombuffer(image_bytes, np.uint8), -1)
    # decoded = cv.rotate(decoded, cv.ROTATE_180)
    # cv.imwrite('../testing/tulemus2.png', result)

