import os
import subprocess
from PIL import Image
from pdf2image import convert_from_path
from random import choices


def generate_lily_file(i):
    possible_notes = ['c\'', 'd\'', 'e\'', 'f\'', 'g\'', 'a\'', 'b\'', 'c\'\'']
    with open('files\{}.ly'.format(i), 'w') as file:
        notes = choices(possible_notes)
        file.write('\\version "2.18.2"\n{\n')
        file.write('{}\n'.format(' '.join(notes)))
        file.write('}')

iterations = 5

for i in range(iterations):
    generate_lily_file(i)
    os.system(r'path "C:\Program Files (x86)\LilyPond\usr\bin"')
    os.system(r'lilypond -o files\{} files\{}.ly'.format(i, i))

    PDFFILE = 'files\{}.pdf'.format(i)

    images = convert_from_path(PDFFILE,
                               poppler_path=r"C:\Users\Kristiina\Downloads\poppler-0.68.0_x86\poppler-0.68.0\bin")
    for image in images:
        width, height = image.size

        # Setting the points for cropped image
        left = 0
        top = 0
        right = width / 2
        bottom = height / 6

        # Cropped image of above dimension
        # (It will not change orginal image)
        im1 = image.crop((left, top, right, bottom))
        im1.save('files\{}.png'.format(i))
        # image.save("proov.png")

# Size of the image in pixels (size of orginal image)
# # (This is not mandatory)
# width, height = image.size
#
# # Setting the points for cropped image
# left = 0
# top = 0
# right = width / 2
# bottom = height / 6
#
# # Cropped image of above dimension
# # (It will not change orginal image)
# im1 = im.crop((left, top, right, bottom))
# im1.save("new.png")


# images = convert_from_path('test2.pdf', poppler_path=r"C:\Users\Kristiina\Downloads\poppler-0.68.0_x86\poppler-0.68.0\bin")
# for image in images:
#     image.save("proov.png")
