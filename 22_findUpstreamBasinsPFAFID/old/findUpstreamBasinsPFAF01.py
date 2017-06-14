"""
CATCHMENT LEVEL FLOW ACCUMULATION
September 19, 2015 ; March 17 2017
Author: Tianyi Luo ; Rutger Hofste
"""

import pandas as pd
import numpy as np
import os, ftplib, urllib2
from datetime import datetime, timedelta

# Settings
# Before you run the script, make sure the columns are in the right dtype (int64)


inputLocation = "C:\Users\Rutger.Hofste\Desktop\werkmap\level6\hybas_merged_standard_level6_V01.csv"
outputLocation = "C:\Users\Rutger.Hofste\Desktop\werkmap\output\hybas_merged_standard_level6_V01_upstreamV15.csv"
#TARGET_BASIN = 2060022970

#basin_ids =  [TARGET_BASIN]

df = pd.read_csv(inputLocation)

header = df.dtypes

df["HYBAS_ID"] = df["HYBAS_ID"].astype(int)
df["NEXT_DOWN"] = df["NEXT_DOWN"].astype(int)


# testing purposes
#df = df[0:100]


def find_upstream_catchments(basin_ids, df):
    all_up_catchments =[]
    for i in np.arange(1, df.shape[0], 1):
        if not basin_ids:
            break
        else:
            up_catchments_adjacent = []
            for bid in basin_ids:
                bid = int(bid)
                up_ids_idx = df[df['NEXT_DOWN'] == bid]
                up_ids_idx = up_ids_idx.index.tolist()
                for idx in up_ids_idx :
                    up_id = df.HYBAS_ID[idx]
                    up_catchments_adjacent.append(int(up_id))
            basin_ids = up_catchments_adjacent
            all_up_catchments = all_up_catchments + basin_ids

    all_up_catchments_PFAF = df.loc[df.HYBAS_ID.isin(all_up_catchments)].PFAF_ID.tolist()
    return all_up_catchments,all_up_catchments_PFAF

def generate_dictionary(df, outputLocation):
    df_temp = df
    up_catchments = []
    up_catchments_PFAF = []
    for bid in df.HYBAS_ID:
        (all_up_catchments, all_up_catchments_PFAF) = find_upstream_catchments([bid], df)
        up_catchments.append(all_up_catchments)
        up_catchments_PFAF.append(all_up_catchments_PFAF)
        print bid



    df_temp['Upstream_HYBAS_IDs'] = up_catchments
    df_temp['Upstream_PFAF_IDs'] = up_catchments_PFAF
    print "Done, writing file"
    df_temp.to_csv(outputLocation)


generate_dictionary(df, outputLocation)

#find_upstream_catchments([1060001510], df)


print "done"