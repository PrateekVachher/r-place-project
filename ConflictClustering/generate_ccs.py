from generate_pcs import *
import multiprocessing
import pandas as pd

def ccs_score(x):
    result = []
    p = pcs_score
    
    for y in range(2,len(pcs_score)-2):
        value = p[x][y] + level_1_ccs*(p[x+1][y]+p[x+1][y+1]+p[x+1][y-1]+p[x][y+1]+p[x][y-1]+p[x-1][y]+p[x-1][y+1]+p[x-1][y-1])
        value += level_2_ccs *(p[x+2][y] + p[x+2][y+1] + p[x+2][y+2] + p[x+2][y-1] + p[x+2][y-2]+p[x-2][y]+p[x-2][y+1]+p[x-2][y+2]+p[x-2][y-1]+p[x-2][y-2]+p[x-1][y+2]+p[x][y+2]+p[x+1][y+2]+p[x-1][y-2]+p[x][y-2]+p[x+1][y-2])
        result.append(value)
    
    return result

def calculate_ccs(pcs_matrix):
    pool = multiprocessing.Pool(12)
    data = pool.map(ccs_score, range(2,len(pcs_matrix)-2))
    pool.close()
    return pd.DataFrame(data)

frame_number = 0
time_24 = 1491065400
time_window = 10 * 60                                  # In MINUTES
level_1_ccs = 0.5
level_2_ccs = 0.25

pcs_score = pd.DataFrame(index=[x for x in range(1001)], columns=[x for x in range(1001)]).fillna(0)
start_time = time_24 + (frame_number)*60

calculate_pcs_score(start_time, pcs_score)

result = calculate_ccs(pcs_score.values)

print (result)