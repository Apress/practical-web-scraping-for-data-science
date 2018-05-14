import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load our stored results
with open('forum_posts.pkl', "rb") as input_file:
    posts = pickle.load(input_file)

def add_interaction(users, fu, tu):
    if fu not in users:
        users[fu] = {}
    if tu not in users[fu]:
        users[fu][tu] = 0
    users[fu][tu] += 1 

# Create interactions dictionary
users = {}
for thread in posts:
    first_one = None
    for post in thread:
        user = post[0]
        quoted = post[1]
        if not first_one:
            first_one = user
        elif not quoted:
            add_interaction(users, user, first_one)
        else:
            for qu in quoted:
                add_interaction(users, user, qu)
    
df = pd.DataFrame.from_dict(users, orient='index').fillna(0)

heatmap = plt.pcolor(df, cmap='Blues')
y_vals = np.arange(0.5, len(df.index), 1)
x_vals = np.arange(0.5, len(df.columns), 1)
plt.yticks(y_vals, df.index)
plt.xticks(x_vals, df.columns, rotation='vertical')
for y in range(len(df.index)):
    for x in range(len(df.columns)):
        if df.iloc[y, x] == 0:
            continue
        plt.text(x + 0.5, y + 0.5, '%.0f' % df.iloc[y, x],
                 horizontalalignment='center',
                 verticalalignment='center')
plt.show()