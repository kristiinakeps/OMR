from flask import Flask, request, jsonify
from random import choice
import string
import recognition, predict
import os
import base64

app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))

@app.route('/', methods=['POST'])
def omr():
    req_data = request.get_json()
    base64image = req_data['image']
    random_name = generate_random_name()
    save_image_to_file(base64image, random_name)

    notes = recognition.music_from_file("{}.png".format(random_name))
    predict.create_music_files(notes, random_name)

    response = create_response(random_name)
    delete_temporary_files(random_name)

    return jsonify(response)

def save_image_to_file(base64image, filename):
    with open("{}.png".format(filename), "wb") as f:
        f.write(base64.b64decode(base64image))

def create_response(filename):
    with open("{}.midi".format(filename), "rb") as midi_file:
        base64_predicted_midi = base64.b64encode(midi_file.read())
    response = {"midi": base64_predicted_midi.decode()}
    return response

def generate_random_name():
    random_name = name_generator()
    while "{}.png".format(random_name) in os.listdir("."):
        random_name = name_generator()
    return random_name

def name_generator(size=8):
    return ''.join([choice(string.ascii_letters + string.digits) for n in range(size)])

def delete_temporary_files(filename):
    os.remove("{}.png".format(filename))
    os.remove("{}.pdf".format(filename))
    os.remove("{}.midi".format(filename))
    os.remove("{}.ly".format(filename))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=port)