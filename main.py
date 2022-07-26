import pandas as pd
datapath = "C:\\Users\\mirar\\Documents\\Cours\\Keio University\\Spring 2022\\Advanced Course in Computer Visualization\\FinalReport\\data\\stories.pkl"
df = pd.read_pickle(datapath)
print(df.head())