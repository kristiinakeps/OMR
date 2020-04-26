import cv2 as cv
import numpy as np
import constants

"""Uses edge detection to find edges in the picture and Hough Line Transform to find lines,
    lowers the number of points that have to be on the line for it to be considered a line
    until at least 5 lines have been detected or the number of points is less than 200.
    Uses the check_lines_horizontal method and remove_lines_too_close methods.
    :param: grayscale image
    :return: list of staff line y-coordinates"""


def staff_detection(img):
    edges = cv.Canny(img, 50, 150, apertureSize=3)
    points_on_line = 400
    lines = cv.HoughLines(edges, 1, np.pi / 180, points_on_line)
    while lines is None or len(lines) < 5 and points_on_line >= 200:
        points_on_line -= 50
        lines = cv.HoughLines(edges, 1, np.pi / 180, points_on_line)
    horizontal_lines = check_lines_horizontal(lines)
    if len(horizontal_lines) > 0:
        cleaned_lines = remove_lines_too_close(horizontal_lines)
        return cleaned_lines
    return []


"""Removes lines that are not horizontal, the maximum difference in degrees is in the constant MAX_DIFFERENCE_DEGREE.
    :param: list of staff line y-coordinates
    :return: list of staff line y-coordinates that contains only horizontal lines"""


def check_lines_horizontal(lines):
    line_y_coordinates = []
    for el in lines:
        rho, theta = el[0]
        if (theta > (np.pi / 2 - constants.MAX_DIFFERENCE_DEGREE * np.pi / 180)) and (
                theta < (np.pi / 2 + constants.MAX_DIFFERENCE_DEGREE * np.pi / 180)):
            line_y_coordinates.append(rho)
    return line_y_coordinates


"""Removes the lines that are too close, the minimum disctance the lines must have in order to 
    not be considered the same is in the MIN_DISTANCE_BETWEEN_LINES constant.
    :param: list of staff line y-coordinates
    :return: list of staff lines that have sufficient space between them"""


def remove_lines_too_close(lines):
    lines.sort()
    cleaned_lines = []
    cleaned_lines.append(lines[0])
    for i in range(1, len(lines)):
        if abs(lines[i] - cleaned_lines[-1]) > constants.MIN_DISTANCE_BETWEEN_LINES:
            cleaned_lines.append(lines[i])
    return cleaned_lines


"""Finds the most frequent distance between two consecutive lines.
    :param: list of staff line y-coordinates
    :return: most frequent distance as float"""


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
    :param: staff line y-coordinates
    :return: coordinates and notes dictionary"""


def group_and_identify(staffs, space, size_difference, is_treble):
    staffs = [round(staff * size_difference) for staff in staffs]
    grouped = group_lines(staffs, space)
    identified, rows = identify_lines(grouped, space, is_treble)
    return identified, rows


"""Groups tha staff lines that are close together (distance is less than the most frequent space + min distance between lines).
    :param: list of staff line y-coodinates, space between lines
    :return: two dimentsional array of grouped lines"""


def group_lines(staffs, space):
    grouped = [[]]
    grouped[-1].append(staffs[0])
    for i in range(1, len(staffs)):
        if abs(staffs[i] - grouped[-1][-1]) < space + constants.MIN_DISTANCE_BETWEEN_LINES:
            grouped[-1].append(staffs[i])
        else:
            grouped.append([staffs[i]])
    grouped = [group for group in grouped if len(group) > 1]
    return grouped


""" Assigns note heights to each line, also adds coodinates for the 
    notes that are in between two staff lines or above or below them.
    :param: two dimentional array of grouped lines, space between lines
    :return: dictionary of coordinates and the note heights, start and end y-coordinate tuple of each row"""


def identify_lines(grouped, space, is_treble):
    coordinates_and_notes = {}
    row_start_and_end = []
    notes_on_line_and_above = constants.NOTES_ON_LINES_TREBLE + constants.NOTES_ABOVE_TOP_LINE_TREBLE if is_treble else \
        constants.NOTES_ON_LINES_BASS + constants.NOTES_ABOVE_TOP_LINE_BASS
    for group in grouped:
        coordinates_and_notes_for_row = {}
        index_of_last_note_on_line = (len(group) - 1) * 2 - 1
        for i in range(15):  # number of notes on the lines, between them and up to the third ledger line
            if i < index_of_last_note_on_line:
                index = -1 - i // 2
                if i % 2 == 0:  # note in on the line
                    coordinates_and_notes_for_row[group[index]] = notes_on_line_and_above[i]
                else:
                    coordinates_and_notes_for_row[group[index] + (group[index - 1] - group[index]) / 2] = \
                    notes_on_line_and_above[i]
            elif i == index_of_last_note_on_line:
                coordinates_and_notes_for_row[group[0]] = notes_on_line_and_above[i]
            else:
                coordinates_and_notes_for_row[group[0] - (i - index_of_last_note_on_line + 1) * space / 2] = \
                notes_on_line_and_above[i]
        notes_below_bottom_line = constants.NOTES_BELOW_BOTTOM_LINE_TREBLE if is_treble else constants.NOTES_BELOW_BOTTOM_LINE_BASS
        for i in range(0, 6):  # notes below the bottom line
            coordinates_and_notes_for_row[group[-1] + (i + 1) * space / 2] = notes_below_bottom_line[i]
        row_start_and_end.append((min(coordinates_and_notes_for_row.keys()), max(coordinates_and_notes_for_row.keys())))
        coordinates_and_notes.update(coordinates_and_notes_for_row)
    return coordinates_and_notes, row_start_and_end
