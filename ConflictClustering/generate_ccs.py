from generate_pcs import *
from generate_clusters import *
import multiprocessing, pickle, os
import pandas as pd
from tqdm import tqdm


import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)



def ccs_score(x):
    result = []
    p = pcs_score
    
    for y in range(2,len(pcs_score)-2):
        value = p[x][y] + level_1_ccs*(p[x+1][y]+p[x+1][y+1]+p[x+1][y-1]+p[x][y+1]+p[x][y-1]+p[x-1][y]+p[x-1][y+1]+p[x-1][y-1])
        value += level_2_ccs *(p[x+2][y] + p[x+2][y+1] + p[x+2][y+2] + p[x+2][y-1] + p[x+2][y-2]+p[x-2][y]+p[x-2][y+1]+p[x-2][y+2]+p[x-2][y-1]+p[x-2][y-2]+p[x-1][y+2]+p[x][y+2]+p[x+1][y+2]+p[x-1][y-2]+p[x][y-2]+p[x+1][y-2])
        result.append(value)
    
    return result

def calculate_ccs(pcs_matrix):
    pool = multiprocessing.Pool(num_cores)
    data = pool.map(ccs_score, range(2,len(pcs_matrix)-2))
    pool.close()
    return pd.DataFrame(data)


# - - - - - - - - - - - - - - Static Variables - - - - - -- - - - - - - - #

time_24 = 1491065400
time_window = 10 * 60                                  # In MINUTES
level_1_ccs = 0.5 / 8
level_2_ccs = 0.25 /16
num_cores = 24
dump_directory = "/home/srivbane/shared/caringbridge/data/projects/place-project/DataResults/"

# - - - - - - - - - - - - - - Iterating over Minute Frames with Window Size 10 minutes - - - - - -- - - - - - - - #

for frame_number in tqdm(range(800,801)):
    pcs_score = pd.DataFrame(index=[x for x in range(1001)], columns=[x for x in range(1001)]).fillna(0)
    
    start_time = time_24 + (frame_number)*60

    calculate_pcs_score(start_time, pcs_score)

    ccs_result = calculate_ccs(pcs_score.values)
    
    
    
    newpath = "{}/CCSResults/hour-{}/".format(dump_directory, str(frame_number//60))
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    
    newpath = "{}/ClusterResults/hour-{}/".format(dump_directory, str(frame_number//60))
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    
    
    pickle.dump(ccs_result, open("{}/CCSResults/hour-{}/ccs-{}.res".format(dump_directory, str(frame_number//60), str(frame_number).zfill(4)), "wb"))

    conflict_regions = identify_conflicts(ccs_result)

    pickle.dump(ccs_result, open("{}/ClusterResults/hour-{}/cluster-{}.res".format(dump_directory, str(frame_number//60), str(frame_number).zfill(4)), "wb"))