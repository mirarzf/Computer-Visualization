import os 
import pandas as pd
import numpy as np 

datafile = "stories.pkl"
df = pd.read_pickle(os.path.join("./data", datafile)) 
# print(df.head())
# print(df.iloc[0])
firstrow = df.iloc[0]
# print(firstrow["clip_frame_idxs"][0].shape)
# print(firstrow["thread_clip_idxs"].shape)


print(df.iloc[2]["video_id"])
# print(df.loc[df["video_id"] == df.iloc[0]["video_id"] ])

firstviddata = df.loc[df["video_id"] == df.iloc[2]["video_id"] ]
# print(firstviddata)

n = len(firstviddata)
for i in range(n): 
    print(firstviddata.iloc[i]["thread_clip_idxs"].shape)

for i in range(n): 
    print("nb of clips", len(firstviddata.iloc[i]["clip_frame_idxs"]))