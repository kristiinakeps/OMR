import cv2 as cv
import numpy as np

def get_locations(img_black_and_white, threshold, template_path, length, template_distance_to_center):  # tähe esinemised pildil
    template = cv.imread(template_path, 0)
    # template = cv.cvtColor(template, cv.COLOR_BGR2GRAY)
    thres, template = cv.threshold(template, 127, 255, cv.THRESH_BINARY)

    res = cv.matchTemplate(img_black_and_white, template, cv.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    new_loc = []

    prev_x, prev_y = (0, 0)  # liiga lähedal asuvaid noote ei taha topelt arvestada
    for pt in zip(*loc[::-1]):
        x, y = pt
        if (abs(x - prev_x) > 2 * template_distance_to_center) or (abs(y - prev_y) > 2 * template_distance_to_center):
            new_loc.append((x, y, length, template_distance_to_center))
        prev_x, prev_y = pt

    # kontrolliks fail tuvastatud asukohtadega
    create_image_with_rectangles_for_template(img_black_and_white, template, loc, length)

    return new_loc

def create_image_with_rectangles_for_template(image, template, loc, length):
    img_rgb_new = image.copy()
    w, h = template.shape[::-1]
    for pt in zip(*loc[::-1]):
        cv.rectangle(img_rgb_new, pt, (pt[0] + w, pt[1] + h), (204, 0, 0), 2)
    cv.imwrite('../testing/tuvastus{}.png'.format(length), img_rgb_new)

def calculate_heights_and_divide_to_rows(locs, coordinates_and_notes, rows):
    heights = [[] for row in rows]
    for el in locs:
        x, y, length, template_distance_to_center = el
        for i in range(len(rows)):
            if rows[i][0] <= y <= rows[i][1]:
                res = calculate_height(el, coordinates_and_notes)
                if res is not None:
                    heights[i].append((x, res, y, length))

    return heights

def divide_to_rows(locs, rows):
    divided = [[] for row in rows]
    for el in locs:
        x, y, length, template_distance_to_center = el
        for i in range(len(rows)):
            if rows[i][0] <= y <= rows[i][1]:
                divided[i].append((x, y, length))
    return divided

def calculate_height(location, coordinates_and_notes):
    x, y, length, template_distance_to_center = location
    note_center_y = y + template_distance_to_center
    closest = min(coordinates_and_notes.keys(), key=lambda x: abs(x-note_center_y))
    return coordinates_and_notes[closest]

def clean_rows(rows):
    cleaned = []
    for row in rows:
        cleaned.append([])
        if len(row) > 0:
            row = sorted(row, key=lambda x: x[0])
            cleaned[-1].append(row[0])
            for i in range(1, len(row)):
                if abs(row[i][0] - cleaned[-1][-1][0]) > 30:  # 30 is the average template width * 1.5
                    cleaned[-1].append(row[i])
    return cleaned

def add_flags_to_notes(note_rows, flag_rows):
    for i in range(len(flag_rows)):
        print(note_rows[i])
        for flag in flag_rows[i]:
            print(flag)
            x, y, length = flag
            note_index = note_rows[i].index(min(note_rows[i], key=lambda el: abs(x - el[0])))
            print(note_index)
            note_rows[i][note_index] = (note_rows[i][note_index][0], note_rows[i][note_index][1], note_rows[i][note_index][2], length)



def recognize_all_symbols(img_black_and_white, coordinates_and_notes, rows):
    quarter_note_path = '../testing/quarter.png'
    locs_quarter = get_locations(img_black_and_white, 0.6, quarter_note_path, 4, 5)
    heights_quarter = calculate_heights_and_divide_to_rows(locs_quarter, coordinates_and_notes, rows)
    cleaned_quarter = clean_rows(heights_quarter)
    print(cleaned_quarter)
    flag_path = '../testing/flag.png'
    locs_flag = get_locations(img_black_and_white, 0.6, flag_path, 8, 5)
    flag_rows = divide_to_rows(locs_flag, rows)
    cleaned_flags = clean_rows(flag_rows)
    print(cleaned_flags)

    add_flags_to_notes(cleaned_quarter, cleaned_flags)

    whole_note_path = '../testing/whole_empty.png'
    locs_whole = get_locations(img_black_and_white, 0.6, whole_note_path, 1, 5)
    heights_whole = calculate_heights_and_divide_to_rows(locs_whole, coordinates_and_notes, rows)
    cleaned_whole = clean_rows(heights_whole)

    half_note_path = '../testing/half_empty.png'
    locs_half = get_locations(img_black_and_white, 0.6, half_note_path, 2, 5)
    heights_half = calculate_heights_and_divide_to_rows(locs_half, coordinates_and_notes, rows)
    cleaned_half = clean_rows(heights_half)
    print(cleaned_half)

    combined = []
    for i in range(len(rows)):
        combined.append([])
        combined[i].extend(cleaned_quarter[i])
        combined[i].extend(cleaned_half[i])
        combined[i].extend(cleaned_whole[i])

    return combined