import cv2 as cv
import numpy as np
from PIL import Image
import os

NOTE_LETTERS = ["c", "d", "e"]
# NOTE_LETTERS = ["c"]
# NOTE_LENGTHS = ["1", "2", "4", "8", "16", "32"]
# NOTE_OCTAVES = ["", "'", "''", "'''"]
NOTE_LENGTHS = ["4"]
NOTE_OCTAVES = ["'"]

# c'4 tuvastab ka kõik e'4 ja e'2
THRES = {"c'4": 0.8, "e'4": 0.85, "d'4": 0.8}
PRIORITY = ["c'4", "e'4", "d'4"]


def get_locations(path, note, threshold):  # tähe esinemised pildil
    img_rgb = cv.imread(path)
    # Muuda mustvalgeks
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    template = cv.imread("templates\\images" + os.path.sep + note + '.png', 0)

    res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    # while len(loc[0]) == 0:  # kui ei leidnud ühtegi tähte, siis vähendame lävendit ja proovime uuesti kuni leiame
    #     threshold -= 0.05
    #     loc = np.where(res >= threshold)
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
    # img_rgb_new.save("testing\\rectangles\\" + note + '.png')
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
            if PRIORITY.index(first[2]) > PRIORITY.index(second[2]):
                choice = first
            else:
                choice = second
        # võrdleme esimese kahe noodi seast valitut ka kolmanda noodiga
        if (abs(third[0] - choice[0]) < 30) and (abs(third[1] - choice[1]) < 30):
            if PRIORITY.index(choice[2]) < PRIORITY.index(third[2]):
                choice = third

        try:
            if new_result[len(new_result) - 1] == choice:
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
        if PRIORITY.index(next_last[2]) < PRIORITY.index(last[2]) and last_in_new_result != last:
            new_result.append(last)
        elif PRIORITY.index(next_last[2]) >= PRIORITY.index(last[2]) and last_in_new_result != next_last:
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
    result.sort(key=lambda el: el[0])
    result = clean_result(result)
    output = [el[2] for el in result]

    return output


if __name__ == "__main__":
    print(lyrics_from_file("testing\\mary_lamb.png"))

    # img_rgb = cv.imread('testing\\mary_had_a_little_lamb.png')
    # # Muuda mustvalgeks
    # img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    #
    # template_rgb = cv.imread("templates\\images\\c'4.png")
    # template = cv.cvtColor(template_rgb, cv.COLOR_BGR2GRAY)
    # # shape: kõrgus-laius
    # # [::-1] keerab mäletatavasti tagurpidi
    # w, h = template.shape[::-1]
    # res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
    # threshold = 0.9
    # loc = np.where(res >= threshold)
    # img_rgb_new = img_rgb.copy()
    #
    # for pt in zip(*loc[::-1]):
    #     # rectangle(pilt, algusnurk (koordinaadid), lõppnurk, värv (BGR), joone paksus)
    #     cv.rectangle(img_rgb_new, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)
    #
    # cv.imshow("pilt3", img_rgb_new)
    # cv.waitKey()
