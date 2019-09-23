from PIL import Image as PILImage
from datetime import datetime
import numpy
import pandas as pd
from tqdm import tqdm

rgb_db = {0: (255, 255, 255), 1: (228, 228, 228), 2: (136, 136, 136), 
          3: (34, 34, 34), 4: (255, 167, 209), 5: (229, 0, 0), 6: (229, 149, 0), 
          7: (160, 106, 66), 8: (229, 217, 0), 9: (148, 224, 68), 10: (2, 190, 1), 
          11: (0, 229, 240), 12: (0, 131, 199), 13: (0, 0, 234), 14: (224, 74, 255), 
          15: (130, 0, 128)}


time = 1491238734

directory = "/home/srivbane/shared/caringbridge/data/projects/place-project/data/"
df = pd.read_feather(directory+"derived/feather/user.ft")

def generate_emptycanvas(x_range,y_range):
    canvas = numpy.zeros((x_range, y_range, 3), dtype=numpy.uint8)
    for x in tqdm(range(x_range)):
        for y in range(y_range):
            canvas[x,y] = (255, 255, 255)   
    return canvas

def board_status(time):
    canvas = generate_emptycanvas(1001,1001)
    data = df[df["timestamp"].between(0, time, inclusive=True)].groupby(["x_coordinate", "y_coordinate"])
    for name, group in data:
        canvas[name[0], name[1]] = rgb_db[group.tail(1)["color"].values[0]]
    return canvas

canvas = board_status(time, window)
image = PILImage.fromarray(canvas)
image.save("img/"+str(time)+".png")