BINARY_THRES = 127

MIN_DISTANCE_BETWEEN_LINES = 10
MAX_DIFFERENCE_DEGREE = 2

NOTES_ON_LINES_TREBLE = ["e'", "f'", "g'", "a'", "b'", "c''", "d''", "e''", "f''"]
NOTES_ABOVE_TOP_LINE_TREBLE = ["g''", "a''", "b''", "c'''", "d'''", "e'''", "f'''", "g'''", "a'''", "b'''"]
NOTES_BELOW_BOTTOM_LINE_TREBLE = ["d'", "c'", "b", "a", "g", "f", "e", "d"]

NOTES_ON_LINES_BASS = ["g,", "a,", "b,", "c", "d", "e", "f", "g", "a"]
NOTES_ABOVE_TOP_LINE_BASS = ["b", "c'", "d'", "e'", "f'", "g'", "a'", "b'", "c''", "d''"]
NOTES_BELOW_BOTTOM_LINE_BASS = ["f,", "e,", "d,", "c,", "b,,", "a,,", "g,,", "f,,"]

KEY_SIGNATURES_SHARP = ['c', 'g', 'd', 'a', 'e', 'b', 'fis']
KEY_SIGNATURES_FLAT = ['c', 'f', 'bes', 'es', 'as', 'des', 'ges']
SHARPS_ORDER = ['f', 'c', 'g', 'd', 'a', 'e']
FLATS_ORDER = ['b', 'e', 'a', 'd', 'g', 'c']
SHARP_SUFFIX = 'is'
FLAT_SUFFIX = 'es'

TEMPOS_AND_PATHS = {'4/4': 'templates/tempo_4_4.png', '3/4': 'templates/tempo_3_4.png',
                    '2/4': 'templates/tempo_2_4.png', '2/2': 'templates/tempo_2_2.png',
                    '6/8': 'templates/tempo_6_8.png'}

QUARTER_NOTE_PATH = 'templates/quarter.png'
WHOLE_NOTE_PATH = 'templates/whole.png'
HALF_NOTE_PATH = 'templates/half.png'

FLAG_8_PATH = 'templates/flag_8.png'
FLAG_8_UPSIDE_PATH = 'templates/flag_8_upside.png'
FLAG_16_PATH = 'templates/flag_16.png'
FLAG_16_UPSIDE_PATH = 'templates/flag_16_upside.png'
CONNECTED_FLAGS_8_PATH = 'templates/connected_8.png'
CONNECTED_FLAGS_16_PATH = 'templates/connected_16.png'

CLEF_TREBLE_PATH = 'templates/clef_treble.png'
CLEF_BASS_PATH = 'templates/clef_bass.png'

SHARP_PATH = 'templates/sharp.png'
FLAT_PATH = 'templates/flat.png'
BECARRE_PATH = 'templates/becarre.png'

REST_1_PATH = "templates/r1.png"
REST_2_PATH = "templates/r2.png"
REST_4_PATH = "templates/r4.png"
REST_8_PATH = "templates/r8.png"
REST_16_PATH = "templates/r16.png"

TEMPOS_THRES = 0.85

QUARTER_NOTE_THRES = 0.6
WHOLE_NOTE_THRES = 0.6
HALF_NOTE_THRES = 0.6

FLAG_8_THRES = 0.65
FLAG_8_UPSIDE_THRES = 0.7
FLAG_16_THRES = 0.6
FLAG_16_UPSIDE_THRES = 0.6
CONNECTED_FLAGS_8_THRES = 0.8
CONNECTED_FLAGS_16_THRES = 0.8

CLEF_THRES = 0.8

KEY_THRES = 0.5

SHARP_THRES = 0.7
FLAT_THRES = 0.7
BECARRE_THRES = 0.7

REST_1_THRES = 0.7
REST_2_THRES = 0.7
REST_4_THRES = 0.7
REST_8_THRES = 0.8
REST_16_THRES = 0.7

QUARTER_NOTE_DISTANCE_TO_CENTER = 5
WHOLE_NOTE_DISTANCE_TO_CENTER = 5
HALF_NOTE_DISTANCE_TO_CENTER = 4

TEMPO_MIN_DISTANCE = 0

NOTE_MIN_DISTANCE = 30

FLAG_MIN_DISTANCE = 30
CONNECTED_FLAGS_MIN_DISTANCE = 10
CONNECTED_FLAGS_8_WIDTH = 39
CONNECTED_FLAGS_16_WIDTH = 34

CLEF_MIN_DISTANCE = 0

ACCIDENTAL_MIN_DISTANCE = 10
MAX_DISTANCE_BETWEEN_ACCIDENTAL_AND_NOTE = 30

REST_1_MIN_DISTANCE = 30
REST_2_MIN_DISTANCE = 30
REST_4_MIN_DISTANCE = 20
REST_8_MIN_DISTANCE = 20
REST_16_MIN_DISTANCE = 25

MIN_DISTANCE_KEY_NOTE = 20
