import glob
from PIL import Image as ImagePIL, ImageFont, ImageDraw

path_url = '/data/flask_bing/App/static/images/*.jpg'
paths = glob.glob(path_url)
for file in paths:
    im = ImagePIL.open(file)
    im.save(file, dpi=(200.0, 200.0))
