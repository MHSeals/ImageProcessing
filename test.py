from PIL import Image
from time import sleep
import os
import Webcam

def test(image):
    print(image);
    im = Image.open(image)
    im.show()
    print(im.format, im.size, im.mode)
    ims = im.split()

    red = ims[0]
    red = red.point(lambda p: 255 if p > 170 else 0)
    red = red.convert('1')
    red.show()

    grn = ims[1]
    #grn = grn.point(lambda p: 255 if p > 170 else 0)
    #grn = grn.convert('1')
    grn.show()

    blu = ims[2]
    #blu = blu.point(lambda p: 255 if p > 170 else 0)
    #blu = red.convert('1')
    blu.show()

testimgs = "./testimages"

# arr = os.listdir(testimgs);
# 
# for img in arr:
#     test(testimgs+"/"+img)
#     exit();

webcam = Webcam.Webcam()
webcam.get_frames()
