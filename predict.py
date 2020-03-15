import recognition
import test_files
import os

BAR = "\\bar\"|\""
TEMPLATE = """\\version "2.20.0"
\score {{
    \\new Staff {{
        \\time 4/4
            {notes}
    }}
    \\midi {{ }}
    \\layout {{ }}
}}"""
FILE_NAME = "testing\\prediction"

def create_music_files(notes):
    note_str = " ".join(notes)
    with open(FILE_NAME + ".ly", 'w') as file:
        file.write(TEMPLATE.format(notes=note_str))
    os.system(r'path "C:\Program Files (x86)\LilyPond\usr\bin"')
    os.system((r'lilypond -o {} {}').format(FILE_NAME, FILE_NAME + ".ly"))
    test_files.get_image_from_pdf(FILE_NAME + ".pdf")


if __name__ == "__main__":
    notes = recognition.lyrics_from_file("testing\\mary_lamb.png")
    create_music_files(notes)