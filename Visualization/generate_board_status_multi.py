from PIL import Image as PILImage
from datetime import datetime
import numpy, multiprocessing
import pandas as pd
from tqdm import tqdm

rgb_db = {0: (255, 255, 255), 1: (228, 228, 228), 2: (136, 136, 136), 
          3: (34, 34, 34), 4: (255, 167, 209), 5: (229, 0, 0), 6: (229, 149, 0), 
          7: (160, 106, 66), 8: (229, 217, 0), 9: (148, 224, 68), 10: (2, 190, 1), 
          11: (0, 229, 240), 12: (0, 131, 199), 13: (0, 0, 234), 14: (224, 74, 255), 
          15: (130, 0, 128)}



directory = "/home/srivbane/shared/caringbridge/data/projects/place-project/data/"

def get_color(y_coordinate):
    global time_func
    temp_df = df[df['y_coordinate'] == y_coordinate]
    list1 = []
    for x_coordinate in range(1001):
        res_df = temp_df[temp_df['x_coordinate'] == x_coordinate]
        color_res = res_df.tail(1)["color"]
        if len(color_res) > 0:
            list1.append(rgb_db[color_res.values[0]])
        else:
            list1.append(rgb_db[0])
    return list1
    
def board_status(time):
    global time_func, df

    df = pd.read_feather(directory+"derived/feather/user.ft")
    df = df[df["timestamp"].between(0, time, inclusive=True)]
    time_func = time
    
    pool = multiprocessing.Pool(24)
    data = pool.map(get_color, range(1001))
    pool.close()
    
    canvas = numpy.array(data).astype('uint8')
    image = PILImage.fromarray(canvas, 'RGB')
    image.save("img/"+str(time)+".png")