from PIL import Image
from pix2tex.cli import LatexOCR

img = Image.open('test.jpg')
model = LatexOCR()
print(model(img))

