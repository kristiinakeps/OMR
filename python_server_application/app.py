from flask import Flask, request, jsonify
from random import choice
import string
import recognition, file_creation, preprocessing, staffs
import os
import base64

app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))

"""Main method that gets the image from the POST request and returns the midi and message.
    :param: none
    :return: json response with midi and message"""


@app.route('/', methods=['POST'])
def omr():
    req_data = request.get_json()
    base64image = req_data['image']
    random_name = generate_random_name()
    image_bytes = base64.b64decode(base64image)
    res = preprocessing.preprocessed_data(image_bytes)
    if res is not None:
        result, staff_lines, space, size_difference = res
        clef = recognition.get_clef(result)
        is_treble = True if clef == 'treble' else False
        coordinates_and_notes, rows = staffs.group_and_identify(staff_lines, space, size_difference, is_treble)
        notes, time_signature, clef, key = recognition.recognize_all_symbols(result, coordinates_and_notes, rows)
        if len(notes) < 1:
            response = create_response("", "Ei suutnud tuvastada ühtegi nooti! Kontrolli, et pilt oleks selge!")
        else:
            file_creation.create_music_files(notes, time_signature, clef, key, random_name)
            midi = get_midi(random_name)
            response = create_response(midi, "")
            delete_temporary_files(random_name)
    else:
        response = create_response("",
                                   "Ei suutnud tuvastada noodijooni. Kontrolli kas noodijooned on pildil sirged ja pilt on selge!")

    return jsonify(response)


"""Creates the response with midi and message.
    :param: midi, message as strings
    :return: response dictionary"""


def create_response(midi, message):
    response = {"midi": midi, "message": message}
    return response


"""Reads the midi from file and encodes it.
    :param: filename
    :return: base64 string midi"""


def get_midi(filename):
    with open("{}.midi".format(filename), "rb") as midi_file:
        base64_predicted_midi = base64.b64encode(midi_file.read())
    return base64_predicted_midi.decode()


"""Returns a random name that's not in use yet.
    :param: none
    :return: random name"""


def generate_random_name():
    random_name = name_generator()
    while "{}.png".format(random_name) in os.listdir("."):
        random_name = name_generator()
    return random_name


"""Generates a random string-
    :param: size of string
    :return: random string"""


def name_generator(size=8):
    return ''.join([choice(string.ascii_letters + string.digits) for n in range(size)])


"""Deletes temporary files that were used during recognition.
    :param: filename
    :return: none"""


def delete_temporary_files(filename):
    os.remove("{}.midi".format(filename))
    os.remove("{}.ly".format(filename))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)
