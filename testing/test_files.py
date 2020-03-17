from pdf2image import convert_from_path
import os


def get_image_from_pdf(path):
    images = convert_from_path(path,
                               poppler_path=r"C:\Users\Kristiina\Downloads\poppler-0.68.0_x86\poppler-0.68.0\bin")
    image_path = path.replace(".pdf", ".png")
    for image in images:
        image.save(image_path)


def generate_testing_file():
    letters = ["c", "d", "e", "f", "g", "a", "b"]
    lengths = ["1", "2", "4"]
    octaves = ["'"]

    notes_by_letter = {}
    for letter in letters:
        notes_by_letter[letter] = [letter + octave + length for octave in octaves for length in lengths]

    notes_by_length = {}
    for length in lengths:
        notes_by_length[length] = [letter + octave + length for letter in letters for octave in octaves]

    bar = "\\bar\"|\""
    letter_str = ""
    for k, v in notes_by_letter.items():
        whole_note = v[0]
        half_notes = " ".join([v[1] for i in range(2)])
        quarter_notes = " ".join([v[2] for i in range(4)])
        letter_str += bar.join([whole_note, half_notes, quarter_notes]) + bar

    length_str = ""
    for k, v in notes_by_length.items():
        if k == "1":
            length_str += bar.join(v) + bar
        if k == "2":
            length_str += bar.join([" ".join([v[i], v[i - 1]]) for i in range(1, len(v))]) + bar
        if k == "4":
            length_str += bar.join([" ".join([v[i], v[i - 1], v[i - 2], v[i - 3]]) for i in range(3, len(v))]) + bar
    template = r"""\version "2.20.0"
\score {{
    \new Staff {{
        \time 4/4
        \cadenzaOn
            {}{}
        \cadenzaOff
    }}
}}""".format(letter_str, length_str)

    with open("test.ly", 'w') as file:
        file.write(template)
    os.system(r'path "C:\Program Files (x86)\LilyPond\usr\bin"')
    os.system(r'lilypond -o testing\test testing\test.ly')

    get_image_from_pdf("test.pdf")


if __name__ == "__main__":
    # get_image_from_pdf("testing\\mary_lamb.pdf")
    generate_testing_file()
