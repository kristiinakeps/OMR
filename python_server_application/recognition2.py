import cv2 as cv
import numpy as np

NOTE_TEMPLATE_HEIGHT = 5


def get_locations(img_black_and_white, threshold):  # tähe esinemised pildil

    template = cv.imread('../testing/quarter.png', 0)

    res = cv.matchTemplate(img_black_and_white, template, cv.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    new_loc = []

    prev_x, prev_y = (0, 0)  # liiga lähedal asuvaid noote ei taha topelt arvestada
    for pt in zip(*loc[::-1]):
        x, y = pt
        if (abs(x - prev_x) > 2 * NOTE_TEMPLATE_HEIGHT) or (abs(y - prev_y) > 2 * NOTE_TEMPLATE_HEIGHT):
            new_loc.append((x, y))
        prev_x, prev_y = pt

    # kontrolliks fail tuvastatud asukohtadega
    create_image_with_rectangles_for_template(img_black_and_white, template, loc)

    return new_loc

def create_image_with_rectangles_for_template(image, template, loc):
    img_rgb_new = image.copy()
    w, h = template.shape[::-1]
    for pt in zip(*loc[::-1]):
        cv.rectangle(img_rgb_new, pt, (pt[0] + w, pt[1] + h), (204, 0, 0), 2)
    cv.imwrite('../testing/tuvastus.png', img_rgb_new)
def calculate_heights(locs, coordinates_and_notes, rows):
    heights = [[] for row in rows]
    for el in locs:
        x, y = el
        for i in range(len(rows)):
            if rows[i][0] <= y <= rows[i][1]:
                res = calculate_height(el, coordinates_and_notes)
                if res is not None:
                    heights[i].append((x, res, y))

    return heights

def calculate_height(location, coordinates_and_notes):
    x, y = location
    note_center_y = y + NOTE_TEMPLATE_HEIGHT
    closest = min(coordinates_and_notes.keys(), key=lambda x: abs(x-note_center_y))
    return coordinates_and_notes[closest]

def clean_rows(rows):
    cleaned = []
    for row in rows:
        if len(row) > 0:
            cleaned.append([])
            row = sorted(row, key=lambda x: x[0])
            cleaned[-1].append(row[0])
            for i in range(1, len(row)):
                if abs(row[i][0] - cleaned[-1][-1][0]) > 2 * NOTE_TEMPLATE_HEIGHT:
                    cleaned[-1].append(row[i])
    return cleaned