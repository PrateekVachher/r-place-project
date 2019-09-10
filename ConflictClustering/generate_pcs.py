import pandas as pd

def swaps(numpyarray):
    swaps_count = 0
    for x in range(len(numpyarray)-1):
        if numpyarray[x] != numpyarray[x+1]:
            swaps_count += 1
    return swaps_count

def pcs(pixel, pcs_score):
    swap_weight = 0.5
    edit_weight = 1
    
    x = pixel["x_coordinate"].values[0]
    y = pixel["y_coordinate"].values[0]
    
    old_pcs_value = pcs_score.iloc[x,y]
    edits = len(pixel)
    swap_values = swaps(pixel["color"].values)
    
    new_pcs_value = (edit_weight*edits) + (swap_weight*swap_values)
    
    pcs_score.set_value(x, y, new_pcs_value)

    
def calculate_pcs_score(time, pcs_score):
    users = df[df["timestamp"].between(time - time_window, time, inclusive=True)].groupby(["x_coordinate", "y_coordinate"])
    users.apply(pcs, pcs_score)

frame_number = 0
time_24 = 1491065400
time_window = 10 * 60                 #In MINUTES

start_time = time_24 + (frame_number)*60

directory = "/home/srivbane/shared/caringbridge/data/projects/place-project/data/"
df = pd.read_feather(directory+"derived/feather/user.ft")