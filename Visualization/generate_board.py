from tqdm import tqdm
import pickle

class Transaction:
    def __init__(self,time,color):
        self.time = time
        self.color = color
    
class Pixel:
    def __init__(self,x,y):
        self.transactions = []
        
    def addTransaction(self, mod):
        self.transactions.append(mod)

def sort_transactions(board):
    for x in tqdm(range(len(board))):
        for y in range(len(board[x])):
            pixel = board[x][y]
            pixel.transactions.sort(key=lambda x: x.time, reverse=False)
    return board

def create_empty_canvas(x_range,y_range):
    canvas = []
    for x in range(x_range):
        row = []
        for y in range(y_range):
            row.append(Pixel(x,y))
        canvas.append(row)
    return canvas
        
        
canvas = create_empty_canvas(1001,1001)

print ("Initialized Board")
    
directory = "/home/srivbane/shared/caringbridge/data/projects/place-project/data/"
document = open(directory+"raw/place/tile_placements_with_usernames.csv","r").readlines()
first = document[0]
document = document[1:]

for x in tqdm(range(len(document))):

    i = document[x].split(",")
    
    timestamp = int(i[0])//1000
    x = int(i[3])
    y = int(i[4])
    color = int(i[5])
    
    canvas[x][y].addTransaction(Transaction(timestamp, color))

print ("Transactions added to Canvas")

print ("Starting Transaction Sort")

board = sort_transactions(canvas)

print ("Saving DataSet to File")
pickle.dump(canvas, open("board.dat", "wb"))

print ("Successful Processing")