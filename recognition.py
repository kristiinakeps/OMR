from collections import defaultdict
from random import shuffle
import cv2 as cv
import numpy as np
import os

NOTE_LETTERS = ["c", "d", "e", "f", "g", "a", "b"]
NOTE_LENGTHS = ["1", "2", "4"]
NOTE_OCTAVES = ["'"]

# mallide lävendite jaoks on vaikeväärtus 0.8, osadele on määratud käsitsi
THRES = defaultdict(lambda: 0.8)
THRES_VALUES = {"c'1": 0.7, "c'2": 0.72, "c'4": 0.83,
                "d'1": 0.75, "d'2": 0.74, "d'4": 0.8,
                "e'2": 0.77, "e'4": 0.87,
                "f'2": 0.77, "f'4": 0.9,
                "g'1": 0.75, "g'2": 0.75, "g'4": 0.85,
                "a'4": 0.85, "a'2": 0.75,
                "b'2": 0.77, "b'4": 0.85
                }
for k, v in THRES_VALUES.items():
    THRES[k] = v

PRIORITY = ["c'4", "e'4", "d'4", "g'4"]
PRIORITY_PAIRS = [("c'1", "e'1"), ("c'2", "c'4"), ("c'2", "e'2"), ("c'2", "e'2"), ("c'4", "e'2"), ("c'4", "e'4"),
                  ("d'2", "d'4"), ("d'4", "f'4"),
                  ("e'2", "e'4"),
                  ("f'2", "f'4"),
                  ("g'2", "c'2"), ("g'2", "g'4"), ("g'4", "e'4"),
                  ("a'4", "a'2")
                  ]

COLORS = [(220, 20, 60), (255, 0, 0), (205, 92, 92), (240, 128, 128), (255, 69, 0), (255, 165, 0), (255, 215, 0),
          (154, 205, 50),
          (107, 142, 35), (124, 252, 0), (0, 100, 0), (50, 205, 50), (0, 255, 127), (32, 178, 170), (0, 128, 128),
          (0, 255, 255),
          (127, 255, 212), (100, 149, 237), (0, 191, 255), (30, 144, 255), (25, 25, 112), (65, 105, 225), (75, 0, 130),
          (138, 43, 226), (72, 61, 139), (147, 112, 219), (148, 0, 211), (186, 85, 211), (128, 0, 128), (238, 130, 238),
          (255, 105, 180),
          (244, 164, 96), (139, 69, 19), (188, 143, 143), (176, 196, 222)
          ]


def get_locations(path, note, threshold):  # tähe esinemised pildil
    img_rgb = cv.imread(path)
    # Muuda mustvalgeks
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    template = cv.imread("modified_templates" + os.path.sep + note + '.png', 0)

    res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    new_loc = []

    prev_x, prev_y = (0, 0)  # liiga lähedal asuvaid noote ei taha topelt arvestada
    for pt in zip(*loc[::-1]):
        x, y = pt
        if (abs(x - prev_x) > 30) or (abs(y - prev_y) > 30):
            new_loc.append((x, y))
        prev_x, prev_y = pt

    img_rgb_new = img_rgb.copy()
    w, h = template.shape[::-1]
    for pt in zip(*loc[::-1]):
        # rectangle(pilt, algusnurk (koordinaadid), lõppnurk, värv (BGR), joone paksus)
        cv.rectangle(img_rgb_new, pt, (pt[0] + w, pt[1] + h), (204, 0, 0), 2)
    cv.imwrite("testing\\rectangles\\" + note + '.png', img_rgb_new)
    return new_loc


def clean_result(result):
    # puhastatud tulemusjärjend
    new_result = []
    # vaatame läbi kõik kolmikud
    for i in range(2, len(result)):
        first = result[i - 2]
        second = result[i - 1]
        third = result[i]

        # kolmest noodist valituks osutunud
        choice = first
        # esimese kahe noodi kontroll, kui asuvad liiga lähestikuu, siis vaatame prioriteetide järjendist kumba eelistame
        if (abs(second[0] - first[0]) < 30) and (abs(second[1] - first[1]) < 30):
            if (second[2], first[2]) in PRIORITY_PAIRS:
                choice = first
            else:
                choice = second
        # võrdleme esimese kahe noodi seast valitut ka kolmanda noodiga
        if (abs(third[0] - choice[0]) < 30) and (abs(third[1] - choice[1]) < 30):
            if (choice[2], third[2]) in PRIORITY_PAIRS:
                choice = third
        try:
            # kui puhastatud järjendis viimane noot on liiga lähedal hetkel valitule, siis seda ei lisa
            if new_result[len(new_result) - 1] == choice or (abs(new_result[len(new_result) - 1][0] - choice[0]) < 30) \
                    and (abs(new_result[len(new_result) - 1][1] - choice[1]) < 30):
                pass
            else:
                new_result.append(choice)
        except:
            new_result.append(choice)

    # viimased kaks nooti käsitsi üle kontrollida
    next_last = result[len(result) - 2]
    last = result[len(result) - 1]
    last_in_new_result = new_result[len(new_result) - 1]
    if abs(next_last[0] - last[0]) < 30 and abs(next_last[1] - last[1]) < 30:
        if (next_last[2], last[2]) in PRIORITY_PAIRS and last_in_new_result != last:
            new_result.append(last)
        elif (last[2], next_last[2]) in PRIORITY_PAIRS and last_in_new_result != next_last:
            new_result.append(next_last)
    else:
        if last_in_new_result != next_last and last_in_new_result != last:
            new_result.append(next_last)
            new_result.append(last)
        elif last_in_new_result == next_last:
            new_result.append(last)
    return new_result


def lyrics_from_file(filename):
    notes = [note + octave + length for note in NOTE_LETTERS for octave in NOTE_OCTAVES for length in NOTE_LENGTHS]
    result = []
    for note in notes:
        loc = get_locations(filename, note, THRES[note])
        result += [(x, y, note) for (x, y) in loc]  # järjendisse lisatakse koordinaadid koos vastava tähega
    result.sort(key=lambda el: el[1])  # sorteerime kõik y-koordinaatide järgi, et saada ridade järgi järjestust
    rows = [[]]
    y = 0  # hoiame meeles eelmise y-koordnaadi
    for res in result:
        if abs(res[
                   1] - y) > 50:  # kui uue elemendi y-koordinaat erineb rohkem kui 50 võrra, siis eeldame et alustasime uue reaga
            rows.append([])  # iga rea jaoks uus järjend
        rows[-1].append(res)  # lisame viimasesse ritta
        y = res[1]
    rows = [sorted(row, key=lambda el: el[0]) for row in rows]
    flatten_rows = [el for row in rows for el in row]
    result = clean_result(flatten_rows)
    create_image_with_rectangles(filename, result)
    output = [el[2] for el in result]

    return output

def create_image_with_rectangles(image_path, locations):
    img = cv.imread(image_path)
    w, h = 50, 130
    shuffle(COLORS)
    notes = [letter + octave + length for letter in NOTE_LETTERS for octave in NOTE_OCTAVES for length in NOTE_LENGTHS]
    colors = dict(zip(notes, COLORS[:len(notes)]))
    for x, y, note in locations:
        # rectangle(pilt, algusnurk (koordinaadid), lõppnurk, värv (BGR), joone paksus)
        cv.rectangle(img, (x, y), (x + w, y+ h), colors[note], 2)
    cv.imwrite("testing\\rectangles\\result.png", img)


if __name__ == "__main__":
    print(lyrics_from_file("testing\\mary_lamb.png"))
