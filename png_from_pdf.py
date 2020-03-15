from pdf2image import convert_from_path

pdf_file = "testing\\mary_lamb.pdf"

images = convert_from_path(pdf_file, poppler_path=r"C:\Users\Kristiina\Downloads\poppler-0.68.0_x86\poppler-0.68.0\bin")

for image in images:
    image_path = "testing\\mary_lamb.png"
    image.save(image_path)