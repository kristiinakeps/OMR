import os

BAR = "\\bar\"|\""
TEMPLATE = """\\version "2.18.0"
\score {{
    \\new Staff {{
        \\time 4/4
            {notes}
    }}
    \\midi {{ }}
    \\layout {{ }}
}}"""

# testimiseks
FILE_NAME = "testing" + os.pathsep + "prediction"

def create_music_files(notes, filename=FILE_NAME):
    note_str = " ".join(notes)
    with open(filename + ".ly", 'w') as file:
        file.write(TEMPLATE.format(notes=note_str))

    # Windowsi jaoks tuleb path ka määrata
    # os.system(r'path "{}"'.format(r"C:\Program Files (x86)\LilyPond\usr\bin"))
    os.system((r'lilypond {}').format(filename, filename + ".ly"))
