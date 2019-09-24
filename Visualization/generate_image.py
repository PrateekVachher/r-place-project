from datetime import datetime
import numpy
import pickle
from tqdm import tqdm
from PIL import Image as PILImage

class Transaction:
    def __init__(self,time,color):
        self.time = time
        self.color = color
    
class Pixel:
    def __init__(self,x,y):
        self.transactions = []
        
    def addTransaction(self, mod):
        self.transactions.append(mod)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

rgb_db = {0: (255, 255, 255), 1: (228, 228, 228), 2: (136, 136, 136), 
          3: (34, 34, 34), 4: (255, 167, 209), 5: (229, 0, 0), 6: (229, 149, 0), 
          7: (160, 106, 66), 8: (229, 217, 0), 9: (148, 224, 68), 10: (2, 190, 1), 
          11: (0, 229, 240), 12: (0, 131, 199), 13: (0, 0, 234), 14: (224, 74, 255), 
          15: (130, 0, 128)}

dataset = pickle.load(open("board.dat", "rb"))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

def generate_emptycanvas(x_range,y_range):
    canvas = numpy.zeros((x_range, y_range, 3), dtype=numpy.uint8)
    for x in tqdm(range(x_range)):
        for y in range(y_range):
            canvas[x,y] = (255, 255, 255)   
    return (canvas)

def generate_image(canvas, time):
    canvas = generate_emptycanvas(1001,1001)

    for x in tqdm(range(len(dataset))):
        for y in range(len(dataset[x])):
            pixel = dataset[x][y]
            if len(pixel.transactions) > 0:
                for transaction in pixel.transactions:
                    if transaction.time <= time:
                        canvas[y,x] = rgb_db[transaction.color]
    image = PILImage.fromarray(canvas)
    image.save("img/"+str(start_time)+".png")
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #