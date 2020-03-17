from flask import Flask, request, jsonify
from random import choice
import string
from python_server_application import recognition, predict
import os
import base64

app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))

FILE_DIR = "predicting_files" + os.pathsep

@app.route('/', methods=['POST'])
def omr():
    req_data = request.get_json()
    base64image = req_data['image']
    random_name = generate_random_name()
    save_image_to_file(base64image, random_name)

    notes = recognition.music_from_file("{}{}.png".format(FILE_DIR, random_name))
    predict.create_music_files(notes, FILE_DIR + random_name)

    response = create_response(random_name)
    # delete_temporary_files(random_name)

    return jsonify(response)

def save_image_to_file(base64image, filename):
    with open("{}{}.png".format(FILE_DIR, filename), "wb") as f:
        f.write(base64.b64decode(base64image))

def create_response(filename):
    with open("{}{}.pdf".format(FILE_DIR, filename), "rb") as image_file:
        base64_predicted_image = base64.b64encode(image_file.read())
    with open("{}{}.mid".format(FILE_DIR, filename), "rb") as midi_file:
        base64_predicted_midi = base64.b64encode(midi_file.read())
    response = {"pdf": base64_predicted_image.decode(), "midi": base64_predicted_midi.decode()}
    return response

def generate_random_name():
    random_name = name_generator()
    while "{}.png".format(random_name) in os.listdir("predicting_files"):
        random_name = name_generator()
    return random_name

def name_generator(size=8):
    return ''.join([choice(string.ascii_letters + string.digits) for n in range(size)])

def delete_temporary_files(filename):
    os.remove("{}{}.png".format(FILE_DIR, filename))
    os.remove("{}{}.pdf".format(FILE_DIR, filename))
    os.remove("{}{}.mid".format(FILE_DIR, filename))
    os.remove("{}{}.ly".format(FILE_DIR, filename))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=port)