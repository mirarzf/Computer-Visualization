import os
from types import new_class 
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 

datafile = "stories.pkl"
df = pd.read_pickle(os.path.join("./data", datafile)) 


# print(df.iloc[2]["video_id"])

firstviddata = df.loc[df["video_id"] == "P35_104" ]
# print(firstviddata)

n = len(firstviddata)
# There are always 10 clips per story 
# The clips are then divided between the different 
# for i in range(n): 
#     print(i)
#     # print("nb of clips", firstviddata.iloc[i]["thread_clip_idxs"])
#     print("nb of threads", len(firstviddata.iloc[i]["clip_frame_idxs"]))
#     print("nb of threads", firstviddata.iloc[i]["clip_frame_idxs"])

# print(firstviddata.iloc[4]["clip_frame_idxs"][0].shape)
# print(firstviddata.iloc[4]["clip_frame_idxs"][1].shape)
# print(firstviddata.iloc[4]["clip_frame_idxs"][2].shape)
# for i in range(3): 
#     print("clip #{}".format(i), firstviddata.iloc[4]["clip_frame_idxs"][i])


# print(firstviddata["video_id"])

## GET THE NUMBER OF THREADS PER STORY 
df["nb_of_threads"] = [len(row["clip_frame_idxs"]) for idx, row in df.iterrows()]
# print(threads_per_story.head())


## SHOW THE TIMELINE OF ONE STORY 
# n = len(df)
# fig = plt.figure() 
# nrows = 15
# print(n)
# ax = fig.subplots(nrows = nrows, ncols = 1)
# for i in range(nrows): #n 
#     xranges = [] 
#     facecolors = []
#     for j in range(df.iloc[i]["nb_of_threads"]): 
#         clips = df.iloc[i]["clip_frame_idxs"][j]
#         # new_xrange = [(clip[0], clip[-1]-clip[0]) for clip in clips]
#         new_xrange = [(clips[0][0], clips[-1][-1]-clips[0][0])]
#         xranges += new_xrange
#         color = np.random.rand(1, 3)
#         facecolors += [color] * len(new_xrange)
#     ax[i].broken_barh(xranges, (0, 10), facecolors = tuple(facecolors)) 
#     ax[i].set_yticks([5], labels = [df.iloc[i]["video_id"]])
#     ax[i].set_xticks([], labels = [])
    
# plt.show()

## HISTOGRAMS OF THE DIFFERENT SPLITS 

# First: Pie chart showing the number of stories per split 
n_train = len( df[ df["split"] == "train" ] )
n_val = len( df[ df["split"] == "val" ] )
n_test = len( df[ df["split"] == "test" ] )
print(n_train, n_val, n_test)


def func(pct, allvalues):
    absolute = int(pct / 100.*np.sum(allvalues))
    return "{:.1f}%\n({:d} stories)".format(pct, absolute)

fig = plt.figure()
ns = [n_train, n_val, n_test]
plt.pie(ns, labels = ["train", "validation", "test"], autopct = lambda pct: func(pct, ns))

# plt.show()

# Second: Histogram showing the distribution of number of threads per story in each split
splits = ["train", "val", "test"]
fig = plt.figure()
fig.set_tight_layout(True)
ax = fig.subplots(nrows = len(splits)+1, ncols = 1)
for i in range(len(splits)): 
    split = splits[i]
    current_ax = ax[i]
    df[df["split"] == split].hist(column=["nb_of_threads"], ax = current_ax, grid = False)
    ax[i].set_title(split)

current_ax = ax[-1]
df.hist(column=["nb_of_threads"], ax = current_ax, grid = False)
current_ax.set_title("Complete dataset")

# plt.show()

## TIMELINE PER VIDEO 
# First: Get all the stories for each video 
df_video_gps = df.groupby(by = ["video_id"]).groups

stories = []
facecolors = []
video_names = [] 
counter = 0 
# splits = {} 
for video in df_video_gps: 
    story = [] 
    threadcolors = []
    for ind, row in df[df["video_id"] == video].iterrows(): 
        # if video in splits.keys() and splits[video] != row["split"]: 
        #     print("AIE")
        #     print(row["split"], splits[video])
        #     break
        # else: 
        #     splits[video] = row["split"]
        for j in range(row["nb_of_threads"]): 
            clips = row["clip_frame_idxs"][j]
            new_xrange = [(clips[0][0], clips[-1][-1]-clips[0][0])]
            story += new_xrange
            color = np.random.rand(1, 3)
            threadcolors += [color] * len(new_xrange)
    stories.append(story)
    facecolors.append(threadcolors)
    video_names.append(video)

df_stories = pd.DataFrame()
df_stories["video_id"] = video_names
df_stories["story"] = stories
df_stories["facecolors"] = facecolors 


print("Input here the index: ")
video_name = input()
datarow = df_stories.loc[df_stories["video_id"] == video_name]
story = datarow["story"].iloc[0]
print(story)
fig = plt.figure(figsize=(5,1.5)) 
ax = fig.subplots(nrows = 1, ncols = 1)
ax.broken_barh(story, (0, 2), facecolors = tuple(df_stories["facecolors"].iloc[0])) 
ax.set_yticks([1], labels = [datarow["video_id"].iloc[0]])
ax.set_ylim(0, 2)
    
plt.show()

