import cv2 as cv
import numpy as np

MIN_DISTANCE_BETWEEN_LINES = 10
MAX_DIFFERENCE_DEGREE = 2

def horizontal_projection(binary_image):
    pixels_in_row = binary_image.shape[1] * 255
    binary_image = 255 - binary_image
    proj = np.sum(binary_image, 1)
    potential_lines = []
    for i in range(len(proj)):
        if proj[i] > 0.7 * pixels_in_row:
            potential_lines.append((i, proj[i]))
    print(potential_lines)
    # Create output image same height as text, 500 px wide
    m = np.max(proj)
    w = 500
    result = np.zeros((proj.shape[0], 500))

    # Draw a line for each row
    for row in range(binary_image.shape[0]):
        cv.line(result, (0, row), (int(proj[row] * w / m), row), (255, 255, 255), 1)
    cv.imwrite('../testing/tulemus.png', result)


def staff_detection(img):
    edges = cv.Canny(img, 50, 150, apertureSize=3)
    points_on_line = 400
    lines = cv.HoughLines(edges, 1, np.pi / 180, points_on_line)
    while len(lines) < 5 and points_on_line >= 200:
        points_on_line -= 50
        lines = cv.HoughLines(edges, 1, np.pi / 180, points_on_line)
    horizontal_lines = check_lines_horizontal(lines)
    if len(horizontal_lines) > 0:
        cleaned_lines = remove_lines_too_close(horizontal_lines)
        return cleaned_lines
    return []
    # for el in lines:
    #     rho, theta = el[0]
        # print(rho)
        # kui nurk on 88 ja 92 kraadi vahel (ehk enam-vähem horisontaalne, täiesti horisontaalne oleks 90)
        # if (theta > (np.pi / 2 - 2 * np.pi / 180)) and (theta < (np.pi / 2 + 2 * np.pi / 180)):
            # y koordinaat on enam-vähem võrdne rhoga
    #
    #     print(rho)
    #     a = np.cos(theta)
    #     b = np.sin(theta)
    #     x0 = a * rho
    #     y0 = b * rho
    #     x1 = int(x0 + width * (-b))
    #     y1 = int(y0 + width * (a))
    #     x2 = int(x0 - width * (-b))
    #     y2 = int(y0 - width * (a))
    #
    #     cv.line(img, (x1, y1), (x2, y2), (0, 0, 255), 1)
    #
    # cv.imwrite('../testing/tulemus.png', img)

def check_lines_horizontal(lines):
    line_y_coordinates = []
    # print((np.pi / 2 + 2 * np.pi / 180))
    # print((np.pi / 2 - 2 * np.pi / 180))
    for el in lines:
        rho, theta = el[0]
        # print(rho)
        # kui nurk on 88 ja 92 kraadi vahel (ehk enam-vähem horisontaalne, täiesti horisontaalne oleks 90)
        if (theta > (np.pi / 2 - MAX_DIFFERENCE_DEGREE * np.pi / 180)) and (theta < (np.pi / 2 + MAX_DIFFERENCE_DEGREE * np.pi / 180)):
            # y koordinaat on enam-vähem võrdne rhoga
            line_y_coordinates.append(rho)
            # a = np.cos(theta)
            # b = np.sin(theta)
            # x0 = a * rho
            # y0 = b * rho
            # x1 = int(x0 + width * (-b))
            # y1 = int(y0 + width * (a))
            # x2 = int(x0 - width * (-b))
            # y2 = int(y0 - width * (a))
            # print(x1, y1, x2, y2)
            #
            # cv.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
    return line_y_coordinates

def remove_lines_too_close(lines):
    lines.sort()
    cleaned_lines = []
    cleaned_lines.append(lines[0])
    for i in range(1, len(lines)):
        if abs(lines[i] - cleaned_lines[-1]) > MIN_DISTANCE_BETWEEN_LINES:
            cleaned_lines.append(lines[i])
    return cleaned_lines

def find_space_between_lines(lines):
    spaces = []
    for i in range(len(lines)-1):
        spaces.append(lines[i+1] - lines[i])
    frequency = {}
    for space in spaces:
        if space not in frequency:
            frequency[space] = 1
        else:
            frequency[space] += 1
    # frequency_grouped = {}
    # keys = list(frequency.keys())
    # keys.sort()
    # for key in keys:
    #     added = False
    #     for i in range(-3, 3):
    #         if key + i in frequency_grouped:
    #             frequency_grouped[key + i] += frequency[key]
    #             added = True
    #             break
    #     if not added:
    #         frequency_grouped[key] = frequency[key]
    # return max(frequency_grouped, key=frequency_grouped.get)
    return  max(frequency, key=frequency.get)






