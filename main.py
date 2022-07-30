import os
from types import new_class 
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.figure import Figure

datafile = "stories.pkl"
df = pd.read_pickle(os.path.join("./data", datafile)) 


## GET THE NUMBER OF THREADS PER STORY 
df["nb_of_threads"] = [len(row["clip_frame_idxs"]) for idx, row in df.iterrows()]


## SHOW THE TIMELINE OF ONE STORY 
def show_first_stories(): 
    n = len(df)
    fig = plt.figure() 
    nrows = 15
    print(n)
    ax = fig.subplots(nrows = nrows, ncols = 1)
    for i in range(nrows): #n 
        xranges = [] 
        facecolors = []
        for j in range(df.iloc[i]["nb_of_threads"]): 
            clips = df.iloc[i]["clip_frame_idxs"][j]
            new_xrange = [(clip[0], clip[-1]-clip[0]) for clip in clips]
            # new_xrange = [(clips[0][0], clips[-1][-1]-clips[0][0])]
            xranges += new_xrange
            color = np.random.rand(1, 3)
            facecolors += [color] * len(new_xrange)
        ax[i].broken_barh(xranges, (0, 10), facecolors = tuple(facecolors)) 
        ax[i].set_yticks([5], labels = [df.iloc[i]["video_id"]])
        ax[i].set_xticks([], labels = [])

## HISTOGRAMS OF THE DIFFERENT SPLITS 

# First: Pie chart showing the number of stories per split 
n_train = len( df[ df["split"] == "train" ] )
n_val = len( df[ df["split"] == "val" ] )
n_test = len( df[ df["split"] == "test" ] )
print(n_train, n_val, n_test)


def func(pct, allvalues):
    absolute = int(pct / 100.*np.sum(allvalues))
    return "{:.1f}%\n({:d} stories)".format(pct, absolute)

def pie_chart(): 
    fig = Figure(figsize=(4,4))
    ax = fig.subplots(nrows = 1, ncols = 1)
    n_train = len( df[ df["split"] == "train" ] )
    n_val = len( df[ df["split"] == "val" ] )
    n_test = len( df[ df["split"] == "test" ] )
    ns = [n_train, n_val, n_test]
    ax.pie(ns, labels = ["train", "validation", "test"], autopct = lambda pct: func(pct, ns))
    return fig 

# Second: Histogram showing the distribution of number of threads per story in each split

def histo_split(split = "total"): 
    fig = Figure()
    ax = fig.subplots(nrows = 1, ncols = 1)
    if split == "total": 
        maximum = max(df["nb_of_threads"])
        minimum = min(df["nb_of_threads"])
        somme = sum(df["nb_of_threads"])
        mean = somme/len(df["nb_of_threads"])
        bins = [i+0.5 for i in range(minimum-1, maximum+1)]
        df.hist(column=["nb_of_threads"], bins = bins, ax = ax, grid = False, edgecolor = '#666', color='#888')
        ax.axvline(mean, color="#222", label="Average number of threads in a story")
    else: 
        maximum = max(df[df["split"] == split]["nb_of_threads"])
        minimum = min(df[df["split"] == split]["nb_of_threads"])
        somme = sum(df[df["split"] == split]["nb_of_threads"])
        mean = somme/len(df[df["split"] == split]["nb_of_threads"])
        bins = [i+0.5 for i in range(minimum-1, maximum+1)]
        df[df["split"] == split].hist(column=["nb_of_threads"], bins = bins, ax = ax, grid = False, edgecolor = '#666', color='#888')
        ax.axvline(mean, color="#222", label="Average number of threads in a story")
    ax.set_title("Repartition of number of threads in a story")
    ax.set_xticks(range(minimum, maximum+1))
    ax.legend(loc="best")
    return fig 

def histo_split_stacked(): 
    fig = Figure()
    ax = fig.subplots(nrows = 1, ncols = 1)
    splits = ["train", "val", "test"]
    maximum = max(df["nb_of_threads"])
    minimum = min(df["nb_of_threads"])
    somme = sum(df["nb_of_threads"])
    mean = somme/len(df["nb_of_threads"])

    columns_splits = [df[df["split"] == split]["nb_of_threads"] for split in splits] 
    
    bins = [i+0.5 for i in range(minimum-1, maximum+1)]
    ax.hist(columns_splits, stacked=True, bins = bins, edgecolor = '#666', color = ['#888', '#aaa', '#ccc'], label = splits)
    ax.axvline(mean, color="#222", label="Average number of threads in a story")
    ax.set_title("Repartition of number of threads in a story")
    ax.set_xticks(range(minimum, maximum+1))
    ax.legend(loc="best")
    return fig 

## TIMELINE PER VIDEO 
# First: Get all the stories for each video 
df_video_gps = df.groupby(by = ["video_id"]).groups

stories = []
facecolors = []
video_names = [] 
counter = 0 
for video in df_video_gps: 
    story = [] 
    threadcolors = []
    for ind, row in df[df["video_id"] == video].iterrows(): 
        for j in range(row["nb_of_threads"]): 
            clips = row["clip_frame_idxs"][j]
            new_xrange = [(clip[0], clip[-1]-clip[0]) for clip in clips]
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


def show_stories_from_video(video_name = "P01_09"):     
    datarow = df_stories.loc[df_stories["video_id"] == video_name]
    story = datarow["story"].iloc[0]

    fig = Figure(figsize = (10,1), layout='tight') 
    ax = fig.subplots(nrows = 1, ncols = 1)
    ax.broken_barh(story, (0, 2), facecolors = tuple(df_stories["facecolors"].iloc[0])) 
    ax.set_yticks([], labels = [])
    ax.set_ylim(0, 2)
    ax.set_xlim(left = 0)
    
    return fig 

def individual_info_from_video(video_name = "P01_09"): 
    datarow = df_stories.loc[df_stories["video_id"] == video_name]
    story = datarow["story"].iloc[0]

    nb_of_stories = len(df[df["video_id"] == video_name])
    nb_of_threads = len(story)
    return nb_of_stories, nb_of_threads

def show_timeline(story_id = None): 
    fig = Figure(figsize = (5,1)) 
    ax = fig.add_subplot(1,1,1)
    if story_id == None: 
        row = df.iloc[0]
    else: 
        row = df.loc[df["story_id"] == story_id]        
    xranges = [] 
    facecolors = []
    for j in range(row["nb_of_threads"]): 
        clips = row["clip_frame_idxs"][j]
        new_xrange = [(clip[0], clip[-1]-clip[0]) for clip in clips]
        # new_xrange = [(clips[0][0], clips[-1][-1]-clips[0][0])]
        xranges += new_xrange
        color = np.random.rand(1, 3)
        facecolors += [color] * len(new_xrange)
        
    ax.broken_barh(xranges, (0, 10), facecolors = tuple(facecolors)) 
    ax.set_yticks([5], labels = [row["video_id"]])
    ax.set_xticks([], labels = []) 
    return fig 

def getListOfVideosIn(split): 
    ret = df[df["split"] == split]["video_id"].unique()
    return list(ret)
