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
FILE_NAME = "testing" + os.pathsep + "prediction"
LILYPOND_PATH =  r"C:\Program Files (x86)\LilyPond\usr\bin" #"/usr/local/bin"

def create_music_files(notes, filename=FILE_NAME):
    note_str = " ".join(notes)
    with open(filename + ".ly", 'w') as file:
        file.write(TEMPLATE.format(notes=note_str))
    os.system(r'path "{}"'.format(LILYPOND_PATH))
    os.system((r'lilypond -o {} {}').format(filename, filename + ".ly"))
    # test_files.get_image_from_pdf(filename + ".pdf")
