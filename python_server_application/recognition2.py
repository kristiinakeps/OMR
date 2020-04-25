import cv2 as cv
import numpy as np

KEY_SIGNATURES_SHARP = ['c', 'g', 'd', 'a', 'e', 'b', 'fis']
KEY_SIGNATURES_FLAT = ['c', 'f', 'bes', 'es', 'as', 'des', 'ges']
SHARPS_ORDER = ['f', 'c', 'g', 'd', 'a', 'e']
FLATS_ORDER = ['b', 'e', 'a', 'd', 'g', 'c']
SHARP_SUFFIX = 'is'
FLAT_SUFFIX = 'es'

TEMPOS_AND_PATHS = {'4/4': '../testing/tempo_4_4.png', '3/4': '../testing/tempo_3_4.png',
                    '2/4': '../testing/tempo_2_4.png', '2/2': '../testing/tempo_2_2.png',
                    '6/8': '../testing/tempo_6_8.png'}
QUARTER_NOTE_PATH = '../testing/quarter.png'
WHOLE_NOTE_PATH = '../testing/whole.png'
HALF_NOTE_PATH = '../testing/half.png'
FLAG_8_PATH = '../testing/flag_8.png'
FLAG_8_UPSIDE_PATH = '../testing/flag_8_upside.png'
FLAG_16_PATH = '../testing/flag_16.png'
FLAG_16_UPSIDE_PATH = '../testing/flag_16_upside.png'
CONNECTED_FLAGS_8_PATH = '../testing/connected_8.png'
CONNECTED_FLAGS_16_PATH = '../testing/connected_16.png'
CLEF_TREBLE_PATH = '../testing/clef_treble.png'
CLEF_BASS_PATH = '../testing/clef_bass.png'
SHARP_PATH = '../testing/sharp.png'
FLAT_PATH = '../testing/flat.png'
BECARRE_PATH = '../testing/becarre.png'


def get_locations(img_black_and_white, threshold, template_path, length,
                  template_distance_to_center):
    template = cv.imread(template_path, 0)
    thres, template = cv.threshold(template, 127, 255, cv.THRESH_BINARY)

    res = cv.matchTemplate(img_black_and_white, template, cv.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    new_loc = []

    prev_x, prev_y = (0, 0)
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
    closest = min(coordinates_and_notes.keys(), key=lambda x: abs(x - note_center_y))
    return coordinates_and_notes[closest]


def clean_rows(rows, min_distance):
    cleaned = []
    for row in rows:
        cleaned.append([])
        if len(row) > 0:
            row = sorted(row, key=lambda x: x[0])
            cleaned[-1].append(row[0])
            for i in range(1, len(row)):
                if abs(row[i][0] - cleaned[-1][-1][0]) > min_distance:
                    cleaned[-1].append(row[i])
    return cleaned


def add_flags_to_notes(note_rows, flag_rows):
    for i in range(len(flag_rows)):
        for flag in flag_rows[i]:
            x, y, length = flag
            if len(note_rows[i]) > 0:
                note_index = note_rows[i].index(min(note_rows[i], key=lambda el: abs(x - el[0])))
                note_rows[i][note_index] = (
                    note_rows[i][note_index][0], note_rows[i][note_index][1], note_rows[i][note_index][2], length)


def add_connected_flags_to_notes(note_rows, flag_rows, note_width):
    for i in range(len(flag_rows)):
        for flag in flag_rows[i]:
            x, y, length = flag
            if len(note_rows[i]) > 0:
                note_index = note_rows[i].index(min(min(note_rows[i], key=lambda el: abs(x - el[0])),
                                                    min(note_rows[i], key=lambda el: abs(x + note_width - el[0]))))
                note_rows[i][note_index] = (
                    note_rows[i][note_index][0], note_rows[i][note_index][1], note_rows[i][note_index][2], length)


def recognize_one_symbol(path, threshold, length, distance_to_center, min_distance_between, img, coordinates_and_notes,
                         rows):
    locs = get_locations(img, threshold, path, length, distance_to_center)
    heights = calculate_heights_and_divide_to_rows(locs, coordinates_and_notes, rows)
    cleaned = clean_rows(heights, min_distance_between)
    return cleaned


def recognize_symbol_without_height(path, threshold, length, distance_to_center, min_distance_between, img, rows):
    locs = get_locations(img, threshold, path, length, distance_to_center)
    flag_rows = divide_to_rows(locs, rows)
    cleaned = clean_rows(flag_rows, min_distance_between)
    return cleaned


def get_time_signature(img):
    for tempo in TEMPOS_AND_PATHS:
        locs = get_locations(img, 0.85, TEMPOS_AND_PATHS[tempo], 0, 0)
        if len(locs) > 0:
            return tempo
    return '4/4'


def get_clef(img):
    locs_bass = get_locations(img, 0.8, CLEF_BASS_PATH, 0, 0)
    if len(locs_bass) > 0:
        return 'bass'
    return 'treble'


def get_key(img, rows, notes):
    number_of_sharps = get_number_of_key_accidentals(img, rows, notes, SHARP_PATH)
    if number_of_sharps == 0:
        number_of_flats = get_number_of_key_accidentals(img, rows, notes, FLAT_PATH)
        if number_of_flats > 6:
            return KEY_SIGNATURES_FLAT[-1]
        return KEY_SIGNATURES_FLAT[number_of_flats]
    if number_of_sharps > 6:
        return KEY_SIGNATURES_SHARP[-1]
    return KEY_SIGNATURES_SHARP[number_of_sharps]


def get_number_of_key_accidentals(img, rows, notes, path):
    cleaned = recognize_symbol_without_height(path, 0.5, 0, 0, 10, img, rows)
    number_in_row = []
    for i in range(len(rows)):
        if len(notes[i]) > 0:
            first_coordinate = notes[i][0][0]
            number_in_row.append(len([sharp for sharp in cleaned[i] if sharp[0] < first_coordinate - 20]))
    most_common_number = max(set(number_in_row), key=number_in_row.count)
    return most_common_number


def get_and_add_accidentals_to_notes(img, rows, notes):
    sharps = recognize_symbol_without_height(SHARP_PATH, 0.7, 0, 0, 10, img, rows)
    correct_notes_accidentals(sharps, notes, SHARP_SUFFIX, rows)

    flats = recognize_symbol_without_height(FLAT_PATH, 0.7, 0, 0, 10, img, rows)
    correct_notes_accidentals(flats, notes, FLAT_SUFFIX, rows)

    becarres = recognize_symbol_without_height(BECARRE_PATH, 0.7, 0, 0, 10, img, rows)
    correct_notes_accidentals(becarres, notes, '', rows)

def correct_notes_accidentals(accidentals, notes, suffix, rows):
    for i in range(len(rows)):
        if len(notes[i]) > 0:
            for accidental in accidentals[i]:
                x, y, length = accidental
                note_index = notes[i].index(min(notes[i], key=lambda el: abs(x - el[0])))
                if abs(notes[i][note_index][0] - x) < 30:
                    if suffix == '':
                        new_note = notes[i][note_index][1].replace(SHARP_SUFFIX, "").replace(FLAT_SUFFIX, "")
                    else:
                        new_note = notes[i][note_index][1][0] + suffix + notes[i][note_index][1][1:]
                    notes[i][note_index] = (notes[i][note_index][0], new_note, notes[i][note_index][2],  notes[i][note_index][3])


def get_notes_and_pauses(img, coordinates_and_notes, rows):
    quarter = recognize_one_symbol(QUARTER_NOTE_PATH, 0.6, 4, 5, 30, img, coordinates_and_notes, rows)
    flags_8 = recognize_symbol_without_height(FLAG_8_PATH, 0.65, 8, 5, 30, img, rows)
    flags_8_upside = recognize_symbol_without_height(FLAG_8_UPSIDE_PATH, 0.7, 8, 5, 30, img, rows)
    flags_16 = recognize_symbol_without_height(FLAG_16_PATH, 0.6, 16, 5, 30, img, rows)
    flags_16_upside = recognize_symbol_without_height(FLAG_16_UPSIDE_PATH, 0.6, 16, 5, 30, img, rows)
    connected_flags_8 = recognize_symbol_without_height(CONNECTED_FLAGS_8_PATH, 0.8, 8, 0, 10, img, rows)
    connected_flags_16 = recognize_symbol_without_height(CONNECTED_FLAGS_16_PATH, 0.8, 16, 0, 10, img, rows)

    add_flags_to_notes(quarter, flags_8)
    add_flags_to_notes(quarter, flags_8_upside)
    add_flags_to_notes(quarter, flags_16)
    add_flags_to_notes(quarter, flags_16_upside)
    add_connected_flags_to_notes(quarter, connected_flags_8, 39)
    add_connected_flags_to_notes(quarter, connected_flags_16, 34)

    whole = recognize_one_symbol(WHOLE_NOTE_PATH, 0.6, 1, 5, 30, img, coordinates_and_notes, rows)
    half = recognize_one_symbol(HALF_NOTE_PATH, 0.6, 2, 4, 30, img, coordinates_and_notes, rows)

    combined = []
    for i in range(len(rows)):
        combined.append([])
        combined[i].extend(quarter[i])
        combined[i].extend(half[i])
        combined[i].extend(whole[i])
        combined[i].sort(key=lambda el: el[0])
    return combined


def correct_note_heights_key(key, notes):
    if key == 'c':
        return
    is_sharp = key in KEY_SIGNATURES_SHARP
    suffix = SHARP_SUFFIX if is_sharp else FLAT_SUFFIX
    accidentals = SHARPS_ORDER[:KEY_SIGNATURES_SHARP.index(key)] if is_sharp else FLATS_ORDER[
                                                                                  :KEY_SIGNATURES_FLAT.index(key)]
    for row in range(len(notes)):
        for note in range(len(notes[row])):
            if notes[row][note][1][0] in accidentals:
                new_note = notes[row][note][1][0] + suffix + notes[row][note][1][1:]
                notes[row][note] = notes[row][note][0], new_note, notes[row][note][2], notes[row][note][3]


def recognize_all_symbols(img_black_and_white, coordinates_and_notes, rows):
    time_signature = get_time_signature(img_black_and_white)
    clef = get_clef(img_black_and_white)

    combined = get_notes_and_pauses(img_black_and_white, coordinates_and_notes, rows)

    key = get_key(img_black_and_white, rows, combined)
    correct_note_heights_key(key, combined)
    get_and_add_accidentals_to_notes(img_black_and_white, rows, combined)

    for row in combined:
        for el in row:
            if len(el[1]) > 2 or el[1] == "b'":
                y = -10
            else:
                y = 30
            img_black_and_white = cv.putText(img_black_and_white, el[1] + str(el[3]), (el[0], el[2] + y),
                                             cv.FONT_HERSHEY_DUPLEX, 0.75, (0, 0, 255), 1)
    cv.imwrite('../testing/tuvastus_perfektne.png', img_black_and_white)

    return combined
