import os
from random import choices, randint

from pdf2image import convert_from_path


def generate_lily_file(i):
    possible_notes = ['c\'', 'd\'', 'e\'', 'f\'', 'g\'', 'a\'', 'b\'', 'c\'\'']
    with open('files\{}.ly'.format(i), 'w') as file:
        notes = choices(possible_notes, k=randint(1, 8))
        file.write('\\version "2.18.2"\n{\n')
        file.write('{}\n'.format(' '.join(notes)))
        file.write('}')


iterations = 500

for i in range(iterations):
    generate_lily_file(i)
    os.system(r'path "C:\Program Files (x86)\LilyPond\usr\bin"')
    os.system(r'lilypond -o files\{} files\{}.ly'.format(i, i))

    PDFFILE = 'files\{}.pdf'.format(i)

    images = convert_from_path(PDFFILE,
                               poppler_path=r"C:\Users\Kristiina\Downloads\poppler-0.68.0_x86\poppler-0.68.0\bin")
    for image in images:
        width, height = image.size

        left = 0
        top = 0
        right = width / 2
        bottom = height / 8

        cropped_image = image.crop((left, top, right, bottom))
        cropped_image.save('files\{}.png'.format(i))
