import cv2 as cv
import numpy as np

MIN_DISTANCE_BETWEEN_LINES = 10
MAX_DIFFERENCE_DEGREE = 2

NOTES_ON_LINES_TREBLE = ["e'", "f'", "g'", "a'", "b'", "c''", "d''", "e''", "f''"]
NOTES_ABOVE_TOP_LINE_TREBLE = ["g''", "a''", "b''", "c'''", "d'''", "e'''", "f'''", "g'''", "a'''", "b'''"]
NOTES_BELOW_BOTTOM_LINE_TREBLE = ["d'", "c'", "b", "a", "g", "f", "e", "d"]

NOTES_ON_LINES_BASS = ["g,", "a,", "b,", "c", "d", "e", "f", "g", "a"]
NOTES_ABOVE_TOP_LINE_BASS = ["b", "c'", "d'", "e'", "f'", "g'", "a'", "b'", "c''", "d''"]
NOTES_BELOW_BOTTOM_LINE_BASS = ["f,", "e,", "d,", "c,", "b,,", "a,,", "g,,", "f,,"]


def horizontal_projection(binary_image):
    pixels_in_row = binary_image.shape[1] * 255
    binary_image = 255 - binary_image
    proj = np.sum(binary_image, 1)
    potential_lines = []
    for i in range(len(proj)):
        if proj[i] > 0.7 * pixels_in_row:
            potential_lines.append((i, proj[i]))
    # Create output image same height as text, 500 px wide
    m = np.max(proj)
    w = 500
    result = np.zeros((proj.shape[0], 500))

    # Draw a line for each row
    for row in range(binary_image.shape[0]):
        cv.line(result, (0, row), (int(proj[row] * w / m), row), (255, 255, 255), 1)
    cv.imwrite('../testing/tulemus.png', result)


"""Uses edge detection to find edges in the picture and Hough Line Transform to find lines,
    lowers the number of points that have to be on the line for it to be considered a line
    until at least 5 lines have been detected or the number of points is less than 200.
    Uses the check_lines_horizontal method and remove_lines_too_close methods.
    arguments: grayscale image
    returns: list of staff line y-coordinates"""


def staff_detection(img):
    edges = cv.Canny(img, 50, 150, apertureSize=3)
    points_on_line = 400
    lines = cv.HoughLines(edges, 1, np.pi / 180, points_on_line)
    while lines is None or len(lines) < 5 and points_on_line >= 200:
        points_on_line -= 50
        lines = cv.HoughLines(edges, 1, np.pi / 180, points_on_line)

    for el in lines:
        width, height = img.shape
        rho, theta = el[0]
        if (theta > (np.pi / 2 - 2 * np.pi / 180)) and (theta < (np.pi / 2 + 2 * np.pi / 180)):
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + width * (-b))
            y1 = int(y0 + width * (a))
            x2 = int(x0 - width * (-b))
            y2 = int(y0 - width * (a))

            cv.line(img, (x1, y1), (x2, y2), (204, 0, 0), 1)

    cv.imwrite('../testing/tulemus.png', img)

    horizontal_lines = check_lines_horizontal(lines)
    if len(horizontal_lines) > 0:
        cleaned_lines = remove_lines_too_close(horizontal_lines)
        return cleaned_lines
    return []



"""Removes lines that are not horizontal, the maximum difference in degrees is in the constant MAX_DIFFERENCE_DEGREE.
    arguments: list of staff line y-coordinates
    returns: list of staff line y-coordinates that contains only horizontal lines"""


def check_lines_horizontal(lines):
    line_y_coordinates = []
    # print((np.pi / 2 + 2 * np.pi / 180))
    # print((np.pi / 2 - 2 * np.pi / 180))
    for el in lines:
        rho, theta = el[0]
        # print(rho)
        # kui nurk on 88 ja 92 kraadi vahel (ehk enam-vähem horisontaalne, täiesti horisontaalne oleks 90)
        if (theta > (np.pi / 2 - MAX_DIFFERENCE_DEGREE * np.pi / 180)) and (
                theta < (np.pi / 2 + MAX_DIFFERENCE_DEGREE * np.pi / 180)):
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


"""Removes the lines that are too close, the minimum disctance the lines must have in order to 
    not be considered the same is in the MIN_DISTANCE_BETWEEN_LINES constant.
    arguments: list of staff line y-coordinates
    returns: list of staff lines that have sufficient space between them"""


def remove_lines_too_close(lines):
    lines.sort()
    cleaned_lines = []
    cleaned_lines.append(lines[0])
    for i in range(1, len(lines)):
        if abs(lines[i] - cleaned_lines[-1]) > MIN_DISTANCE_BETWEEN_LINES:
            cleaned_lines.append(lines[i])
    return cleaned_lines


"""Finds the most frequent distance between two consecutive lines.
    arguments: list of staff line y-coordinates
    returns: most frequent distance as float"""


def find_space_between_lines(lines):
    spaces = []
    for i in range(len(lines) - 1):
        spaces.append(lines[i + 1] - lines[i])
    frequency = {}
    for space in spaces:
        if space not in frequency:
            frequency[space] = 1
        else:
            frequency[space] += 1
    return max(frequency, key=frequency.get)

"""Combines the group_lines and identify_lines methods.
    arguments: staff line y-coordinates
    returns: coordinates and notes dictionary"""
def group_and_identify(staffs, space, size_difference, is_treble):
    staffs = [round(staff * size_difference) for staff in staffs]
    grouped = group_lines(staffs, space)
    identified, rows = identify_lines(grouped, space, is_treble)
    return identified, rows


"""Groups tha staff lines that are close together (distance is less than the most frequent space + min distance between lines).
    arguments: list of staff line y-coodinates, space between lines
    returns: two dimentsional array of grouped lines"""


def group_lines(staffs, space):
    grouped = [[]]
    grouped[-1].append(staffs[0])
    for i in range(1, len(staffs)):
        if abs(staffs[i] - grouped[-1][-1]) < space + MIN_DISTANCE_BETWEEN_LINES:
            grouped[-1].append(staffs[i])
        else:
            grouped.append([staffs[i]])
    grouped = [group for group in grouped if len(group) > 1]
    return grouped


""" Assigns note heights to each line, also adds coodinates for the 
    notes that are in between two staff lines or above or below them.
    arguments: two dimentional array of grouped lines, space between lines
    returns: dictionary of coordinates and the note heights, start and end y-coordinate tuple of each row"""


def identify_lines(grouped, space, is_treble):
    coordinates_and_notes = {}
    row_start_and_end = []
    notes_on_line_and_above = NOTES_ON_LINES_TREBLE + NOTES_ABOVE_TOP_LINE_TREBLE if is_treble else NOTES_ON_LINES_BASS + NOTES_ABOVE_TOP_LINE_BASS
    for group in grouped:
        coordinates_and_notes_for_row = {}
        index_of_last_note_on_line = (len(group) - 1) * 2 - 1
        for i in range(15):  # number of notes on the lines, between them and up to the third ledger line
            if i < index_of_last_note_on_line:
                index = -1 - i // 2
                if i % 2 == 0: # note in on the line
                    coordinates_and_notes_for_row[group[index]] = notes_on_line_and_above[i]
                else:
                    coordinates_and_notes_for_row[group[index] + (group[index - 1] - group[index]) / 2] = notes_on_line_and_above[i]
            elif i == index_of_last_note_on_line:
                coordinates_and_notes_for_row[group[0]] = notes_on_line_and_above[i]
            else:
                coordinates_and_notes_for_row[group[0] - (i - index_of_last_note_on_line + 1) * space / 2] = notes_on_line_and_above[i]
        notes_below_bottom_line = NOTES_BELOW_BOTTOM_LINE_TREBLE if is_treble else NOTES_BELOW_BOTTOM_LINE_BASS
        for i in range(0, 6):  # notes below the bottom line
            coordinates_and_notes_for_row[group[-1] + (i + 1) * space / 2] = notes_below_bottom_line[i]
        row_start_and_end.append((min(coordinates_and_notes_for_row.keys()), max(coordinates_and_notes_for_row.keys())))
        coordinates_and_notes.update(coordinates_and_notes_for_row)
    return coordinates_and_notes, row_start_and_end
