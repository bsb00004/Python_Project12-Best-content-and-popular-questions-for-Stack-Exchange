#!/usr/bin/env python
# coding: utf-8

# Python_Project12:- Best content popular questions for Stack Exchange
# The Goal this project is to use Data Science Stack Exchange to determine what content should a [data science](https://datascience.stackexchange.com/) education company create, based on interest by subject

#### Exploring the Data ####
# Looking at the of each row, it stands out that __FavouriteCount__ has missing values. 
# What other issues are there with the data? Let's explore it.
# We also trying to answer these questions:
# - How many missing values are there in each column?
# - Can we fix the missing values somehow?
# - Are the types of each column adequate?
# - What can we do about the Tags column?

# First, We can read in the data while immediately making sure CreationDate will be stored as a datetime object.
# We import everything that we'll use

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().magic('matplotlib inline')

# making sure CreationDate will be stored as a datetime object
questions = pd.read_csv("2019_questions.csv", parse_dates=["CreationDate"])

#Running questions.info() should gives a lot of useful information.
questions.info()

# We see that only __FavoriteCount__ has missing values. A missing value on this column probably means that 
# the question was is not present in any users' favorite list, so we can replace the missing values with zero.
# The types seem adequate for every column, however, after we fill in the missing values on FavoriteCount, 
# there is no reason to store the values as floats.

# Since the object dtype is a catch-all type, let's see what types the objects in questions["Tags"] are.
# Clean the Tags column and assign it back to itself:
# Use the process illustrated above.
# Assing the result to questions["Tags"].
questions["Tags"].apply(lambda value: type(value)).unique()


# We see that every value in this column is a string. On Stack Exchange, each question can only have a maximum of five tags (source), 
# so one way to deal with this column is to create five columns in questions called 
# Tag1, Tag2, Tag3, Tag4, and Tag5 and populate the columns with the tags in each row.
# However, since doesn't help is relating tags from one question to another, we'll just keep them as a list.

#### Cleaning the Data ####
# We'll begin by fixing FavoriteCount.
questions.fillna(value={"FavoriteCount": 0}, inplace=True)
questions["FavoriteCount"] = questions["FavoriteCount"].astype(int)
questions.dtypes


# Let's now modify Tags to make it easier to work with.
questions["Tags"] = questions["Tags"].str.replace("^<|>$", "").str.split("><")
questions.sample(3)


# We now focus on determining the most popular tags. We'll do so by considering two different popularity proxies: 
# for each tag we'll count how many times the tag was used, and how many times a question with that tag was viewed.
# We could take into account the score, or whether or not a question is part of someone's favorite questions. 
# These are all reasonable options to investigate; but we'll limit the focus of our research to counts and views for now.

#### Most Used and Most Viewed ####
# We'll begin by counting how many times each tag was used
tag_count = dict()
for tags in questions["Tags"]:
    for tag in tags:
        if tag in tag_count:
            tag_count[tag] += 1
        else:
            tag_count[tag] = 1

# For improved aesthetics, let's transform tag_count in a dataframe.
tag_count = pd.DataFrame.from_dict(tag_count, orient="index")
tag_count.rename(columns={0: "Count"}, inplace=True)
tag_count.head(10)

# Let's now sort this dataframe by Count and visualize the top 20 results.
most_used = tag_count.sort_values(by="Count").tail(20)
most_used


# The threshold of 20 is somewhat arbitrary and we can experiment with others, however, popularity of the tags rapidly declines, 
# so looking at these tags should be enough to help us with our goal. Let's visualize these data.
most_used.plot(kind="barh", figsize=(16,8))


# Some tags are very, very broad and are unlikely to be useful; e.g.: python, dataset, r. 
# Before we investigate the tags a little deeper, let's repeat the same process for views.

# We'll use Python's builtin enumerate() function. Its utility is well understood by seeing it action.
some_iterable = "Iterate this!"

for i,c in enumerate(some_iterable):
    print(i,c)
    
# In addition to the elements of some_iterable, enumerate gives us the index of each of them.
tag_view_count = dict()
for idx, tags in enumerate(questions["Tags"]):
    for tag in tags:
        if tag in tag_view_count:
            tag_view_count[tag] += questions["ViewCount"].iloc[idx]
        else:
            tag_view_count[tag] = 1            
tag_view_count = pd.DataFrame.from_dict(tag_view_count, orient="index")
tag_view_count.rename(columns={0: "ViewCount"}, inplace=True)
most_viewed = tag_view_count.sort_values(by="ViewCount").tail(20)
most_viewed.plot(kind="barh", figsize=(16,8))


# Let's see them side by side.
fig, axes = plt.subplots(nrows=1, ncols=2)
fig.set_size_inches((24, 10))
most_used.plot(kind="barh", ax=axes[0], subplots=True)
most_viewed.plot(kind="barh", ax=axes[1], subplots=True)

in_used = pd.merge(most_used, most_viewed, how="left", left_index=True, right_index=True)
in_viewed = pd.merge(most_used, most_viewed, how="right", left_index=True, right_index=True)
 
#### Relations Between Tags ####
# One way of trying to gauge how pairs of tags are related to each other, 
# is to count how many times each pair appears together. Let's do this.


# We'll begin by creating a list of all tags.
all_tags = list(tag_count.index)


# We'll now create a dataframe where each row will represent a tag, and each column as well. Something like this:
#  |**tag1**|**tag2**|**tag3**
# :-----:|:-----:|:-----:|:-----:
# tag1| | | 
# tag2| | | 
# tag3| | | 

associations = pd.DataFrame(index=all_tags, columns=all_tags)
associations.iloc[0:4,0:4]

# We will now fill this dataframe with zeroes and then, for each lists of tags in questions["Tags"], we will increment the intervening tags by one.
# The end result will be a dataframe that for each pair of tags, it tells us how many times they were used together.
associations.fillna(0, inplace=True)

for tags in questions["Tags"]:
    associations.loc[tags, tags] += 1


# This dataframe is quite large. Let's focus our attention on the most used tags. 
# We'll add some colors to make it easier to talk about the dataframe.
relations_most_used = associations.loc[most_used.index, most_used.index]

def style_cells(x):
    helper_df = pd.DataFrame('', index=x.index, columns=x.columns)
    helper_df.loc["time-series", "r"] = "background-color: yellow"
    helper_df.loc["r", "time-series"] = "background-color: yellow"
    for k in range(helper_df.shape[0]):
        helper_df.iloc[k,k] = "color: blue"
    
    return helper_df

relations_most_used.style.apply(style_cells, axis=None)


# The cells highlighted in yellow tell us that time-series was used together with r 22 times. The values in blue tell us how many times each of the tags was used. 
# We saw earlier that machine-learning was used 2693 times and we confirm it in this dataframe.
# It's hard for a human to understand what is going on in this dataframe. Let's create a heatmap. 
# But before we do it, let's get rid of the values in blue, otherwise the colors will be too skewed.

for i in range(relations_most_used.shape[0]):
    relations_most_used.iloc[i,i] = pd.np.NaN

plt.figure(figsize=(12,8))
sns.heatmap(relations_most_used, cmap="Greens", annot=False)

#### Enter Domain Knowledge ####
# At the glance of an eye, someone with sufficient domain knowledge can tell that the most popular topic at the moment, 
# as shown by our analysis, is deep learning.
# Before we officially make our recommendation, it would be nice to solidy our findings with additional proof. 

# The file 'all_questions.csv' holds the result of the query below — this query fetches 
# all of the questions ever asked on DSSE, their dates and tags.
 
# In this we will track the interest in deep learning across time. We will:
# Count how many deep learning questions are asked per time period.
# The total amount of questions per time period.
# How many deep learning questions there are relative to the total amount of questions per time period.

# Let's read in the file into a dataframe called __all_questions.csv__. We'll parse the dates at read-time.
all_q = pd.read_csv("all_questions.csv", parse_dates=["CreationDate"])

# We can use the same technique as before to clean the tags column.
all_q["Tags"] = all_q["Tags"].str.replace("^<|>$", "").str.split("><")

# we should decide what tags are deep learning tags.
# The definition of what constitutes a deep learning tag we'll use is: a tag that belongs to 
# the list ["lstm", "cnn", "scikit-learn", "tensorflow", "keras", "neural-network", "deep-learning"].
# This list was obtained by looking at all the tags in most_used and seeing which ones had any relation to deep learning. 

# We'll now create a function that assigns 1 to deep learning questions and 0 otherwise; and we use it.
def class_deep_learning(tags):
    for tag in tags:
        if tag in ["lstm", "cnn", "scikit-learn", "tensorflow",
                   "keras", "neural-network", "deep-learning"]:
            return 1
    return 0

all_q["DeepLearning"] = all_q["Tags"].apply(class_deep_learning)

all_q.sample(5)

# The data-science-techonology landscape isn't something as dynamic to merit daily, weekly, or even monthly tracking. 
# Let's track it quarterly.

# Since we don't have all the data for the first quarter of 2020, we'll get rid of those dates:
all_q = all_q[all_q["CreationDate"].dt.year < 2020]

# Let's create a column that identifies the quarter in which a question was asked.
def fetch_quarter(datetime):
    year = str(datetime.year)[-2:]
    quarter = str(((datetime.month-1) // 3) + 1)
    return "{y}Q{q}".format(y=year, q=quarter)

all_q["Quarter"] = all_q["CreationDate"].apply(fetch_quarter)
all_q.head()


# For the final stretch of this screen, we'll group by quarter and:
# Count the number of deep learning questions.
# Count the total number of questions.
# Compute the ratio between the two numbers above.

quarterly = all_q.groupby('Quarter').agg({"DeepLearning": ['sum', 'size']})
quarterly.columns = ['DeepLearningQuestions', 'TotalQuestions']
quarterly["DeepLearningRate"] = quarterly["DeepLearningQuestions"]\
                                /quarterly["TotalQuestions"]

# The following is done to help with visualizations later.
quarterly.reset_index(inplace=True)
quarterly.sample(5)

ax1 = quarterly.plot(x="Quarter", y="DeepLearningRate",
                    kind="line", linestyle="-", marker="o", color="orange",
                    figsize=(24,12)
                    )

ax2 = quarterly.plot(x="Quarter", y="TotalQuestions",
                     kind="bar", ax=ax1, secondary_y=True, alpha=0.7, rot=45)

for idx, t in enumerate(quarterly["TotalQuestions"]):
    ax2.text(idx, t, str(t), ha="center", va="bottom")
xlims = ax1.get_xlim()

ax1.get_legend().remove()

handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(handles=handles1 + handles2,
           labels=labels1 + labels2,
           loc="upper left", prop={"size": 12})


for ax in (ax1, ax2):
    for where in ("top", "right"):
        ax.spines[where].set_visible(False)
        ax.tick_params(right=False, labelright=False)
        
# It seems that deep learning questions was a high-growth trend since the start of DSSE and it looks like it is plateauing. 
# There is no evidence to suggest that interest in deep learning is decreasing and so we maintain our previous idea of proposing that we create deep learning content.
