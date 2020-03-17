import os
from pdf2image import convert_from_path

# nootide nimed, pikkused ja oktavite tähised
# näiteks teise oktavi 1-löögiline C noot 4/4 taktimõõdus oleks c''4
NOTE_LETTERS = ["c", "d", "e", "f", "g", "a", "b"]
NOTE_LENGTHS = ["1", "2", "4", "8", "16", "32"]
NOTE_OCTAVES = ["", "'", "''", "'''"]

# Lilypondi failis taktijoone tähis
BAR = "\\bar\"|\""

# FILE_DIR on kaust, kuhu tekitatakse mallide loomiseks vajalikud failid
# IMG_DIR on kaust, kuhu tekitatakse mallide pildid
FILE_DIR = "files\\"
IMG_DIR = "images\\"

# Lilypondi faili mall
LILY_FILE_TEMPLATE = """\\version "2.20.0"
\score {{
    \\new Staff {{
        \\time 4/4
        \cadenzaOn
            {notes}
        \cadenzaOff
    }}
}}"""

# Genereerib etteantud nootide sõnega (notes) .ly faili, mille nimeks on selles asuvate nootide pikkus (length)
def generate_lily_file(length, notes):
    with open((FILE_DIR + '{}.ly').format(length), 'w') as file:
        file.write(LILY_FILE_TEMPLATE.format(notes=notes))

# Tagastab etteantud pikkusele vastava nootide järjendi
def get_note_str(length):
    notes = [note + octave + length for note in NOTE_LETTERS for octave in NOTE_OCTAVES]
    return notes

def generate_templates_from_image(x, y, distance, width, height, notes):
    for i in range(len(notes)):
        image_path = "{}{}.png".format(IMG_DIR, notes[i])
        cropped_image = image.crop((x + i * distance, y, x + width + i * distance, y + height))
        cropped_image.save(image_path)

if __name__ == "__main__":
    for length in NOTE_LENGTHS:
        notes = get_note_str(length)
        # noodijoonega eraldatud üksikud noodid
        note_str = BAR.join(notes)
        generate_lily_file(length, note_str)

        file_name = FILE_DIR + length

        # Lilypondi faili põhjal PDF-fail
        os.system(r'path "C:\Program Files (x86)\LilyPond\usr\bin"')
        os.system(r'lilypond -o {} {}.ly'.format(file_name, file_name))

        pdf_file = '{}.pdf'.format(file_name)

        # PDF-failist pilt
        images = convert_from_path(pdf_file, poppler_path=r"C:\Users\Kristiina\Downloads\poppler-0.68.0_x86\poppler-0.68.0\bin")

        for image in images:
            # iga noodipikkuse jaoks on leitud parimad parameetrid mallide asukohtade leidmiseks
            if length == "1":
                # parameetrid iga rea jaoks: esimsese noodi x-koordinaat, y-koordinaat, kaugus järgmise noodini, laius, kõrgus, järjend nootidest
                generate_templates_from_image(300, 0, 98.5, 58, 233, notes[:13])
                generate_templates_from_image(140, 215, 96.5, 58, 233, notes[13:])
            if length == "2":
                generate_templates_from_image(305, 0, 90.5, 50, 233, notes[:14])
                generate_templates_from_image(145, 215, 102, 50, 233, notes[14:])
            if length == "4":
                generate_templates_from_image(302, 30, 45.5, 45, 250, notes)
            if length in ["8", "16", "32"]:
                generate_templates_from_image(304, 30, 45.5, 46, 250, notes)



