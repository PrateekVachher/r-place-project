import numpy as np
import pandas as pd
import scipy
from tqdm import tqdm

def identify_conflicts(df):
    df = (df.values > 0.5).astype(int)

    region_id_counter = 0

    inprogress_regions = {}  # region ids to list of coordinates
    prev_row_active_cols = {}  # map of column ids to region ids
    curr_row_active_cols = {}  # map of column ids to region ids
    
    prev_row_region_ids = {}  # map of region ids to column ids

    dead_region_ids = []

    for y in range(len(df)):
        conflict_inds = df[y].nonzero()[0]

        prev_x = -2
        for x in conflict_inds:
            coord = (x, y)

            if x - 1 == prev_x:
                # continuation of previous column's region
                region_id = curr_row_active_cols[x-1]
                inprogress_regions[region_id].append(coord)
                curr_row_active_cols[x] = region_id
                if x in prev_row_active_cols:
                    # both a continuation of a region in this row and a region in the row above
                    # need to merge two region ids
                    prev_region_id = prev_row_active_cols[x]  # this is the id of the region in the previous row
                    if region_id != prev_region_id:
                        # these are two distinct regions that need to be merged
                        # so we merge in the contents from this row to the region and region id of the previous row
                        merged_coord_list = inprogress_regions[prev_region_id]
                        merged_coord_list.extend(inprogress_regions[region_id])
                        #inprogress_regions[merged_region_id] = merged_coord_list

                        # update pointers of merged region_ids to new merged list
                        #inprogress_regions[region_id] = merged_coord_list
                        #inprogress_regions[region_id2] = merged_coord_list
                        # marking the previous region ids as "dead"
                        del inprogress_regions[region_id]
                        #dead_region_ids.append(region_id2)

                        # updating the current row region id to the new merged region id
                        for col in curr_row_active_cols:
                            if curr_row_active_cols[col] == region_id:
                                curr_row_active_cols[col] = prev_region_id
                        for col in prev_row_active_cols:
                            if prev_row_active_cols[col] == region_id:
                                prev_row_active_cols[col] = prev_region_id

                        #curr_row_active_cols[x] = merged_region_id
                        #curr_row_active_cols[x-1] = merged_region_id
                        #prev_row_active_cols[x] = merged_region_id
            else:  # not an immediate continuation of a conflict in this row
                if x in prev_row_active_cols:  # continuation of a conflict from a region above
                    region_id = prev_row_active_cols[x]
                    inprogress_regions[region_id].append(coord)
                    curr_row_active_cols[x] = region_id
                else:  # new region (as far as we've seen so far in this row)
                    region_id = region_id_counter
                    region_id_counter += 1
                    curr_row_active_cols[x] = region_id
                    inprogress_regions[region_id] = [coord]

            prev_x = x
        prev_row_active_cols = curr_row_active_cols
        curr_row_active_cols = {}

    # we are done searching, identify completed regions from the inprogress_regions list
    completed_regions = []
    for region_id in inprogress_regions:
        if region_id in dead_region_ids:
            continue
        if len(inprogress_regions[region_id]) > 25:    
            completed_regions.append(inprogress_regions[region_id])
    
    return completed_regions