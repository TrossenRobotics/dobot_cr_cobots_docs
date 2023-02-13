import os
from PIL import Image

baseheight = 60
path_to_input = '.'
path_to_output = './../output'

print(f"{len(os.listdir(path_to_input))} images to be resized.")

for image_path in os.listdir(path_to_input):
    if os.path.isdir(image_path):
        pass
    else:
        print(f"resizing: {image_path}.")
        input_path = os.path.join(path_to_input, image_path)
        image_to_resize = Image.open(input_path)
        hpercent = (baseheight/float(image_to_resize.size[1]))
        wsize = int((float(image_to_resize.size[0])*float(hpercent)))
        img = image_to_resize.resize((wsize, baseheight), Image.ANTIALIAS)
        img.save(os.path.join(path_to_output, image_path))

print(f"{len(os.listdir(path_to_output))-1} images resized.")
