import constants
import cv2 as cv
import numpy as np

"""Uses template matching to find possible locations for the given template. Also does the first step of cleaning the 
    output by not adding consecutive notes that are too close together.
    :param:  black and white image. threshold for template, path to template, the length of the note/rest, 
    distance to the center of the note on the template
    :return: list of x, y coordinate pairs"""


def get_locations(img_black_and_white, threshold, template_path, length,
                  template_distance_to_center):
    template = cv.imread(template_path, 0)
    thres, template = cv.threshold(template, constants.BINARY_THRES, 255, cv.THRESH_BINARY)

    res = cv.matchTemplate(img_black_and_white, template, cv.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    new_loc = []

    prev_x, prev_y = (0, 0)
    for pt in zip(*loc[::-1]):
        x, y = pt
        if (abs(x - prev_x) > 2 * template_distance_to_center) or (abs(y - prev_y) > 2 * template_distance_to_center):
            new_loc.append((x, y, length, template_distance_to_center))
        prev_x, prev_y = pt
    return new_loc


"""Draws rectangles around the matches. Useful for testing.
    :param: image, template, locations, length (is used only for naming the file)
    :return: none"""


def create_image_with_rectangles_for_template(image, template, loc, length):
    img_rgb_new = image.copy()
    w, h = template.shape[::-1]
    for pt in zip(*loc[::-1]):
        cv.rectangle(img_rgb_new, pt, (pt[0] + w, pt[1] + h), (204, 0, 0), 2)
    cv.imwrite('../testing/tuvastus{}.png'.format(length), img_rgb_new)


"""Adds the note height to each location and divides the notes to rows. Uses the calculate_heights method to calculate
    the heights.
    :param: locations, dictionary of staff line coordinates and the corresponding note heights, staff line rows
    :return: two-dimensional array of rows with notes"""


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


"""Divides the symbols that don't need heights to rows.
    :param: locations, staff line rows
    :return: two-dimensional array of rows with symbols"""


def divide_to_rows(locs, rows):
    divided = [[] for row in rows]
    for el in locs:
        x, y, length, template_distance_to_center = el
        for i in range(len(rows)):
            if rows[i][0] <= y <= rows[i][1]:
                divided[i].append((x, y, length))
    return divided


"""Finds the corresponding note to a given location. Calculates the smallest distance from the center of the note to a
    staff line or space between the lines.
    :param: location, dictionary of staff line coordinates and corresponding notes
    :return closest note"""


def calculate_height(location, coordinates_and_notes):
    x, y, length, template_distance_to_center = location
    note_center_y = y + template_distance_to_center
    closest = min(coordinates_and_notes.keys(), key=lambda x: abs(x - note_center_y))
    return coordinates_and_notes[closest]


"""Cleans the rows by removing symbols that are too close together.
    :param: rows, min distance that has to be between two symbols
    :return: cleaned rows"""


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


"""Assigns flags to notes and changes the length of the note if a flag is assigned to it.
    :param: note rows, flag rows
     :return: none"""


def add_flags_to_notes(note_rows, flag_rows):
    for i in range(len(flag_rows)):
        for flag in flag_rows[i]:
            x, y, length = flag
            if len(note_rows[i]) > 0:
                note_index = note_rows[i].index(min(note_rows[i], key=lambda el: abs(x - el[0])))
                note_rows[i][note_index] = (
                    note_rows[i][note_index][0], note_rows[i][note_index][1], note_rows[i][note_index][2], length)


"""Adds flags that are connecting several notes to notes and changing the lengths of those notes.
    :param: note rows, flag rows, width of the connected flag template
    :return: none"""


def add_connected_flags_to_notes(note_rows, flag_rows, width):
    for i in range(len(flag_rows)):
        for flag in flag_rows[i]:
            x, y, length = flag
            if len(note_rows[i]) > 0:
                note_index = note_rows[i].index(min(min(note_rows[i], key=lambda el: abs(x - el[0])),
                                                    min(note_rows[i], key=lambda el: abs(x + width - el[0]))))
                note_rows[i][note_index] = (
                    note_rows[i][note_index][0], note_rows[i][note_index][1], note_rows[i][note_index][2], length)


"""Recognizes one symbol by calling the get_locations, calculate_heights_and_divide_to_rows and clean_rows methods.
    :param: path to template, threshold of the template, length of the symbol, distance to the center of the symbol, min 
    distance between symbols, image, dictionary of coordinates and notes, list of rows
    :return: cleaned rows"""


def recognize_one_symbol(path, threshold, length, distance_to_center, min_distance_between, img, coordinates_and_notes,
                         rows):
    locs = get_locations(img, threshold, path, length, distance_to_center)
    heights = calculate_heights_and_divide_to_rows(locs, coordinates_and_notes, rows)
    cleaned = clean_rows(heights, min_distance_between)
    return cleaned


"""Recognizes one symbol without height by calling the get_locations, divide_to_rows and clean_rows methods.
    :param: path to template, threshold of the template, length of the symbol, distance to the center of the symbol, 
    min distance between symbols, image, rows
    :return: cleaned rows"""


def recognize_symbol_without_height(path, threshold, length, distance_to_center, min_distance_between, img, rows):
    locs = get_locations(img, threshold, path, length, distance_to_center)
    rows = divide_to_rows(locs, rows)
    cleaned = clean_rows(rows, min_distance_between)
    return cleaned


"""Finds the time signature, if no time signature is found, then the default 4/4 is returned.
    :param: image
    :return: time signature string"""


def get_time_signature(img):
    for tempo in constants.TEMPOS_AND_PATHS:
        locs = get_locations(img, constants.TEMPOS_THRES, constants.TEMPOS_AND_PATHS[tempo], 0,
                             constants.TEMPO_MIN_DISTANCE)
        if len(locs) > 0:
            return tempo
    return '4/4'


"""Finds the clef. If no bass clef is detected, then returns treble clef.
    :param: image
    :return: clef string"""


def get_clef(img):
    locs_bass = get_locations(img, constants.CLEF_THRES, constants.CLEF_BASS_PATH, 0, constants.CLEF_MIN_DISTANCE)
    if len(locs_bass) > 0:
        return 'bass'
    return 'treble'


"""Finds the key of the melody. Uses the get_number_of_key_accidentals to count the number of sharps and flats
    recognized before the first note.
    :param: image, rows, notes
    :return: key string"""


def get_key(img, rows, notes):
    number_of_sharps = get_number_of_key_accidentals(img, rows, notes, constants.SHARP_PATH)
    if number_of_sharps == 0:
        number_of_flats = get_number_of_key_accidentals(img, rows, notes, constants.FLAT_PATH)
        if number_of_flats > 6:
            return constants.KEY_SIGNATURES_FLAT[-1]
        return constants.KEY_SIGNATURES_FLAT[number_of_flats]
    if number_of_sharps > 6:
        return constants.KEY_SIGNATURES_SHARP[-1]
    return constants.KEY_SIGNATURES_SHARP[number_of_sharps]


"""Finds the number of key accidentals. Returns the most common number found in all rows.
    :param: image, rows, notes, path to the accidental template
    :return: number of accidentals"""


def get_number_of_key_accidentals(img, rows, notes, path):
    cleaned = recognize_symbol_without_height(path, constants.KEY_THRES, 0, 0, constants.ACCIDENTAL_MIN_DISTANCE, img,
                                              rows)
    number_in_row = []
    for i in range(len(rows)):
        if len(notes[i]) > 0:
            first_coordinate = notes[i][0][0]
            number_in_row.append(
                len([sharp for sharp in cleaned[i] if sharp[0] < first_coordinate - constants.MIN_DISTANCE_KEY_NOTE]))
    if len(number_in_row) < 1:
        return 0
    else:
        most_common_number = max(set(number_in_row), key=number_in_row.count)
        return most_common_number


"""Finds accidentals and adds them to notes by using the correct_notes_accidentals method.
    :param: image, rows, notes
    :return: none"""


def get_and_add_accidentals_to_notes(img, rows, notes):
    sharps = recognize_symbol_without_height(constants.SHARP_PATH, constants.SHARP_THRES, 0, 0,
                                             constants.ACCIDENTAL_MIN_DISTANCE, img, rows)
    correct_notes_accidentals(sharps, notes, constants.SHARP_SUFFIX, rows)

    flats = recognize_symbol_without_height(constants.FLAT_PATH, constants.FLAT_THRES, 0, 0,
                                            constants.ACCIDENTAL_MIN_DISTANCE, img, rows)
    correct_notes_accidentals(flats, notes, constants.FLAT_SUFFIX, rows)

    becarres = recognize_symbol_without_height(constants.BECARRE_PATH, constants.BECARRE_THRES, 0, 0,
                                               constants.ACCIDENTAL_MIN_DISTANCE, img, rows)
    correct_notes_accidentals(becarres, notes, '', rows)


"""Finds which note an accidental belongs to and changes the name of that note accordingly.
    :param: accidentals list, notes list, suffix of the accidental, rows
    :return: none"""


def correct_notes_accidentals(accidentals, notes, suffix, rows):
    for i in range(len(rows)):
        if len(notes[i]) > 0:
            for accidental in accidentals[i]:
                x, y, length = accidental
                note_index = notes[i].index(min(notes[i], key=lambda el: abs(x - el[0])))
                if abs(notes[i][note_index][0] - x) < constants.MAX_DISTANCE_BETWEEN_ACCIDENTAL_AND_NOTE:
                    if suffix == '':
                        new_note = notes[i][note_index][1].replace(constants.SHARP_SUFFIX, "").replace(
                            constants.FLAT_SUFFIX, "")
                    else:
                        new_note = notes[i][note_index][1][0] + suffix + notes[i][note_index][1][1:]
                    notes[i][note_index] = (
                        notes[i][note_index][0], new_note, notes[i][note_index][2], notes[i][note_index][3])


"""Finds all notes and adds flags to them.
    :param: image, dictionary of coordinates and notes, rows
    :return: list of all notes in rows"""


def get_notes(img, coordinates_and_notes, rows):
    quarter = recognize_one_symbol(constants.QUARTER_NOTE_PATH, constants.QUARTER_NOTE_THRES, 4,
                                   constants.QUARTER_NOTE_DISTANCE_TO_CENTER, constants.NOTE_MIN_DISTANCE, img,
                                   coordinates_and_notes, rows)
    flags_8 = recognize_symbol_without_height(constants.FLAG_8_PATH, constants.FLAG_8_THRES, 8, 5,
                                              constants.FLAG_MIN_DISTANCE, img, rows)
    flags_8_upside = recognize_symbol_without_height(constants.FLAG_8_UPSIDE_PATH, constants.FLAG_8_UPSIDE_THRES, 8, 5,
                                                     constants.FLAG_MIN_DISTANCE, img, rows)
    flags_16 = recognize_symbol_without_height(constants.FLAG_16_PATH, constants.FLAG_16_THRES, 16, 5,
                                               constants.FLAG_MIN_DISTANCE, img, rows)
    flags_16_upside = recognize_symbol_without_height(constants.FLAG_16_UPSIDE_PATH, constants.FLAG_16_UPSIDE_THRES, 16,
                                                      5, constants.FLAG_MIN_DISTANCE, img, rows)
    connected_flags_8 = recognize_symbol_without_height(constants.CONNECTED_FLAGS_8_PATH,
                                                        constants.CONNECTED_FLAGS_8_THRES, 8, 0,
                                                        constants.CONNECTED_FLAGS_MIN_DISTANCE, img, rows)
    connected_flags_16 = recognize_symbol_without_height(constants.CONNECTED_FLAGS_16_PATH,
                                                         constants.CONNECTED_FLAGS_16_THRES, 16, 0,
                                                         constants.CONNECTED_FLAGS_MIN_DISTANCE, img, rows)

    add_flags_to_notes(quarter, flags_8)
    add_flags_to_notes(quarter, flags_8_upside)
    add_flags_to_notes(quarter, flags_16)
    add_flags_to_notes(quarter, flags_16_upside)
    add_connected_flags_to_notes(quarter, connected_flags_8, constants.CONNECTED_FLAGS_8_WIDTH)
    add_connected_flags_to_notes(quarter, connected_flags_16, constants.CONNECTED_FLAGS_16_WIDTH)

    whole = recognize_one_symbol(constants.WHOLE_NOTE_PATH, constants.WHOLE_NOTE_THRES, 1,
                                 constants.WHOLE_NOTE_DISTANCE_TO_CENTER, constants.NOTE_MIN_DISTANCE, img,
                                 coordinates_and_notes, rows)
    half = recognize_one_symbol(constants.HALF_NOTE_PATH, constants.HALF_NOTE_THRES, 2,
                                constants.HALF_NOTE_DISTANCE_TO_CENTER, constants.NOTE_MIN_DISTANCE, img,
                                coordinates_and_notes, rows)

    combined = []
    for i in range(len(rows)):
        combined.append([])
        combined[i].extend(quarter[i])
        combined[i].extend(half[i])
        combined[i].extend(whole[i])
        combined[i].sort(key=lambda el: el[0])
    return combined


"""Finds all rests.
    :param: image, rows
    :return: list of all rests in rows"""


def get_rests(img, rows):
    rest_1 = [[(rest[0], "r", rest[1], rest[2]) for rest in row] for row in
              recognize_symbol_without_height(constants.REST_1_PATH, constants.REST_1_THRES, 1, 0,
                                              constants.REST_1_MIN_DISTANCE, img, rows)]
    rest_2 = [[(rest[0], "r", rest[1], rest[2]) for rest in row] for row in
              recognize_symbol_without_height(constants.REST_2_PATH, constants.REST_2_THRES, 2, 0,
                                              constants.REST_2_MIN_DISTANCE, img, rows)]
    rest_4 = [[(rest[0], "r", rest[1], rest[2]) for rest in row] for row in
              recognize_symbol_without_height(constants.REST_4_PATH, constants.REST_4_THRES, 4, 0,
                                              constants.REST_4_MIN_DISTANCE, img, rows)]
    rest_8 = [[(rest[0], "r", rest[1], rest[2]) for rest in row] for row in
              recognize_symbol_without_height(constants.REST_8_PATH, constants.REST_8_THRES, 8, 0,
                                              constants.REST_8_MIN_DISTANCE, img, rows)]
    rest_16 = [[(rest[0], "r", rest[1], rest[2]) for rest in row] for row in
               recognize_symbol_without_height(constants.REST_16_PATH, constants.REST_16_THRES, 16, 0,
                                               constants.REST_16_MIN_DISTANCE, img, rows)]
    combined = []
    for i in range(len(rows)):
        combined.append([])
        combined[i].extend(rest_1[i])
        combined[i].extend(rest_2[i])
        combined[i].extend(rest_4[i])
        combined[i].extend(rest_8[i])
        combined[i].extend(rest_16[i])
    return combined


"""Puts the notes in the right key.
    :param: key, notes
    :return: none"""


def correct_note_heights_key(key, notes):
    if key == 'c':
        return
    is_sharp = key in constants.KEY_SIGNATURES_SHARP
    suffix = constants.SHARP_SUFFIX if is_sharp else constants.FLAT_SUFFIX
    accidentals = constants.SHARPS_ORDER[
                  :constants.KEY_SIGNATURES_SHARP.index(key)] if is_sharp else constants.FLATS_ORDER[
                                                                               :constants.KEY_SIGNATURES_FLAT.index(
                                                                                   key)]
    for row in range(len(notes)):
        for note in range(len(notes[row])):
            if notes[row][note][1][0] in accidentals:
                new_note = notes[row][note][1][0] + suffix + notes[row][note][1][1:]
                notes[row][note] = notes[row][note][0], new_note, notes[row][note][2], notes[row][note][3]


"""Creates an image with the names of the recognized notes and rests written below or above them.
    :param list of notes and rests, image
    :return: none"""


def create_image_with_recognized_notes(combined, img_black_and_white):
    for row in combined:
        for el in row:
            if len(el[1]) > 2 or el[1] == "b'":
                y = -10
            else:
                y = 30
            img_black_and_white = cv.putText(img_black_and_white, el[1] + str(el[3]), (el[0], el[2] + y),
                                             cv.FONT_HERSHEY_DUPLEX, 0.75, (0, 0, 255), 1)
    cv.imwrite('../testing/tuvastus_perfektne.png', img_black_and_white)


"""Recognizes all the notes, rests, gets time signautre and clef.
    :param: image, dictionary of coordinates and notes, rows
    :return: flat list of notes, time siganture, clef, key"""


def recognize_all_symbols(img_black_and_white, coordinates_and_notes, rows):
    time_signature = get_time_signature(img_black_and_white)
    clef = get_clef(img_black_and_white)

    combined = get_notes(img_black_and_white, coordinates_and_notes, rows)

    key = get_key(img_black_and_white, rows, combined)
    correct_note_heights_key(key, combined)
    get_and_add_accidentals_to_notes(img_black_and_white, rows, combined)

    rests = get_rests(img_black_and_white, rows)
    for i in range(len(combined)):
        combined[i].extend(rests[i])

    # create_image_with_recognized_notes(combined, img_black_and_white)

    flat = []
    for row in combined:
        row.sort(key=lambda el: el[0])
        flat.extend(row)

    return flat, time_signature, clef, key
