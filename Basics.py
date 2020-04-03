#!/usr/bin/env python
# coding: utf-8

# ### Popular Data Science Questions¶
# The Goal this project is to use Data Science Stack Exchange to determine what content should a [data science](https://datascience.stackexchange.com/) education company create, based on interest by subject.
# 
# ### Stack Exchange
# Stack Exchange hosts sites on a multitude of fields and subjects, including mathematics, physics, philosophy, and [data science!](https://datascience.stackexchange.com/) Here's a sample of the most popular sites:
# <img src="https://dq-content.s3.amazonaws.com/469/se_sites.png">
# [__Stack Exchange__](https://stackexchange.com/sites?view=list#percentanswered)
# 
# If you open the link shared above, you'll find a complete list of Stack Exchange websites sorted by percentage of questions that received answers. At the time of this writing, Data Science Stack Exchange (DSSE) is on the bottom 10 sites with respect to this metric.
# 
# The fact that DSSE is a data science dedicated site (contrarily to the others), coupled with it having a lot of an unanswered questions, makes it an ideal candidate for this investigation. DSSE will be the focus of this project.
# 
# ##### What kind of questions are welcome on this site?
# On DSSE's help center's section on questions , we can read that we should:
# 
# - Avoid subjective questions.
# - Ask practical questions about Data Science — there are adequate sites for theoretical questions.
# - Ask specific questions.
# - Make questions relevant to others.
# 
# All of these characteristics, if employed, should be helpful attributes to our goal.
# 
# In the help center we also learned that in addition to the sites mentioned in the Learn section, there are other two sites that are relevant:
# 
# - [Open Data](https://opendata.stackexchange.com/) (Dataset requests)
# - [Computational Science](https://scicomp.stackexchange.com/) (Software packages and algorithms in applied mathematics)
# 
# ##### What, other than questions, does DSSE's home subdivide into?
# On the home page we can see that we have four sections:
# 
# - [Questions](https://datascience.stackexchange.com/questions) — a list of all questions asked;
# - [Tags](https://datascience.stackexchange.com/tags) — a list of tags (keywords or labels that categorize questions);
# 
# <img src="https://camo.githubusercontent.com/46d9d26dbb54bbfaf2b92b100ec4c5e427708bf2/68747470733a2f2f64712d636f6e74656e742e73332e616d617a6f6e6177732e636f6d2f3436392f746167735f64732e706e67">
# 
# - [Users](https://datascience.stackexchange.com/users) — a list of users;
# - [Unanswered](https://datascience.stackexchange.com/unanswered) — a list of unanswered questions;
# The tagging system used by Stack Exchange looks just like what we need to solve this problem as it allow us to quantify how many questions are asked about each subject.
# 
# Something else we can learn from exploring the help center, is that Stack Exchange's sites are heavily moderated by the community; this gives us some confidence in using the tagging system to derive conclusions.
# 
# ##### What information is available in each post?
# Looking, just as an example, at [this](https://datascience.stackexchange.com/questions/19141/linear-model-to-generate-probability-of-each-possible-output?rq=1) question, some of the information we see is:
# 
# - For both questions and answers:
#     - The posts's score;
#     - The posts's title;
#     - The posts's author;
#     - The posts's body;
# - For questions only:
#     - How many users have it on their "
#     - The last time the question as active;
#     - How many times the question was viewed;
#     - Related questions;
#     - The question's tags;
# 
# ### Stack Exchange Data Explorer
# Perusing the table names, a few stand out as relevant for our goal:
# 
# - Posts
# - PostTags
# - Tags
# - TagSynonyms
# 
# Running a few exploratory queries, leads us to focus our efforts on Posts table.
# <img, src="https://dq-content.s3.amazonaws.com/469/PostTypes.png">
# 
# For examples, the Tags table looked very promising as it tells us how many times each tag was used, but there's no way to tell just from this if the interest in these tags is recent or a thing from the past.
# 
# Note that with the exception of the tags column, the last few columns contain information about how popular the post is — the kind of information we're after.
# 
# | Id  | TagName          | Count | ExcerptPostId | WikiPostId |
# |-----|------------------|-------|---------------|------------|
# | 2   | machine-learning | 6919  | 4909          | 4908       |
# | 46  | python           | 3907  | 5523          | 5522       |
# | 81  | neural-network   | 2923  | 8885          | 8884       |
# | 194 | deep-learning    | 2786  | 8956          | 8955       |
# | 77  | classification   | 1899  | 4911          | 4910       |
# | 324 | keras            | 1736  | 9251          | 9250       |
# | 128 | scikit-learn     | 1303  | 5896          | 5895       |
# | 321 | tensorflow       | 1224  | 9183          | 9182       |
# | 47  | nlp              | 1162  | 147           | 146        |
# | 24  | r                | 1114  | 49            | 48         |
# 
# Since we're only interested in recent posts, we'll limit our analysis to the posts of 2019. (At the time of writing it is early 2020).
# 
# The dataset we'll be using in this project is __2019_questions.csv__, is the one resulting from Running a query against the SEDE DSSE database that extracts the columns listed above for all the questions in 2019 .
# 
# ### Getting the Data
# To get the relevant data we run the following query.
# 
# SELECT Id, CreationDate,
#   Score, ViewCount, Tags,
#   AnswerCount, FavoriteCount
#   FROM posts
#   WHERE PostTypeId = 1 AND YEAR(CreationDate) = 2019;
#  
# Here's what the first few rows look like:
# 
# 
# | Id    | PostTypeId | CreationDate        | Score | ViewCount | Tags                                                              | AnswerCount | FavoriteCount |
# |-------|------------|---------------------|-------|-----------|-------------------------------------------------------------------|-------------|---------------|
# | 44419 | 1          | 2019-01-23 09:21:13 | 1     | 21        | < machine-learning>< data-mining>                                   | 0           |               |
# | 44420 | 1          | 2019-01-23 09:34:01 | 0     | 25        | < machine-learning>< regression>< linear-regression>< regularization> | 0           |               |
# | 44423 | 1          | 2019-01-23 09:58:41 | 2     | 1651      | < python>< time-series>< forecast>< forecasting>                      | 0           |               |
# | 44427 | 1          | 2019-01-23 10:57:09 | 0     | 55        | < machine-learning>< scikit-learn>< pca>                             | 1           |               |
# | 44428 | 1          | 2019-01-23 11:02:15 | 0     | 19        | < dataset>< bigdata>< data>< speech-to-text>                          | 0           |               |

# ### Exploring the Data
# Looking at the of each row, it stands out that __FavouriteCount__ has missing values. What other issues are there with the data? Let's explore it.
# We also trying to answer these questions:
# - How many missing values are there in each column?
# - Can we fix the missing values somehow?
# - Are the types of each column adequate?
# - What can we do about the Tags column?
# 
# First, We can read in the data while immediately making sure CreationDate will be stored as a datetime object.

# In[28]:



# We import everything that we'll use

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

get_ipython().magic('matplotlib inline')


# In[29]:


# making sure CreationDate will be stored as a datetime object
questions = pd.read_csv("2019_questions.csv", parse_dates=["CreationDate"])


# In[30]:



#Running questions.info() should gives a lot of useful information.

questions.info()


# We see that only __FavoriteCount__ has missing values. A missing value on this column probably means that the question was is not present in any users' favorite list, so we can replace the missing values with zero.
# 
# The types seem adequate for every column, however, after we fill in the missing values on FavoriteCount, there is no reason to store the values as floats.
# 
# Since the object dtype is a catch-all type, let's see what types the objects in questions["Tags"] are.

# In[31]:


# Clean the Tags column and assign it back to itself:
# Use the process illustrated above.
# Assing the result to questions["Tags"].
questions["Tags"].apply(lambda value: type(value)).unique()


# We see that every value in this column is a string. On Stack Exchange, each question can only have a maximum of five tags (source), so one way to deal with this column is to create five columns in questions called Tag1, Tag2, Tag3, Tag4, and Tag5 and populate the columns with the tags in each row.
# 
# However, since doesn't help is relating tags from one question to another, we'll just keep them as a list.
# 
# 
# ### Cleaning the Data
# We'll begin by fixing FavoriteCount.

# In[32]:


questions.fillna(value={"FavoriteCount": 0}, inplace=True)
questions["FavoriteCount"] = questions["FavoriteCount"].astype(int)
questions.dtypes


# Let's now modify Tags to make it easier to work with.

# In[33]:


questions["Tags"] = questions["Tags"].str.replace("^<|>$", "").str.split("><")
questions.sample(3)


# We now focus on determining the most popular tags. We'll do so by considering two different popularity proxies: for each tag we'll count how many times the tag was used, and how many times a question with that tag was viewed.
# 
# We could take into account the score, or whether or not a question is part of someone's favorite questions. These are all reasonable options to investigate; but we'll limit the focus of our research to counts and views for now.
# 
# ### Most Used and Most Viewed
# We'll begin by counting how many times each tag was used

# In[34]:


tag_count = dict()

for tags in questions["Tags"]:
    for tag in tags:
        if tag in tag_count:
            tag_count[tag] += 1
        else:
            tag_count[tag] = 1


# 
# For improved aesthetics, let's transform tag_count in a dataframe.

# In[35]:


tag_count = pd.DataFrame.from_dict(tag_count, orient="index")
tag_count.rename(columns={0: "Count"}, inplace=True)
tag_count.head(10)


# Let's now sort this dataframe by Count and visualize the top 20 results.

# In[36]:


most_used = tag_count.sort_values(by="Count").tail(20)
most_used


# The threshold of 20 is somewhat arbitrary and we can experiment with others, however, popularity of the tags rapidly declines, so looking at these tags should be enough to help us with our goal. Let's visualize these data.

# In[37]:


most_used.plot(kind="barh", figsize=(16,8))


# Some tags are very, very broad and are unlikely to be useful; e.g.: python, dataset, r. Before we investigate the tags a little deeper, let's repeat the same process for views.
# 
# We'll use Python's builtin enumerate() function. Its utility is well understood by seeing it action.

# In[38]:


some_iterable = "Iterate this!"

for i,c in enumerate(some_iterable):
    print(i,c)


# In addition to the elements of some_iterable, enumerate gives us the index of each of them.

# In[39]:


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

# In[40]:


fig, axes = plt.subplots(nrows=1, ncols=2)
fig.set_size_inches((24, 10))
most_used.plot(kind="barh", ax=axes[0], subplots=True)
most_viewed.plot(kind="barh", ax=axes[1], subplots=True)


# In[41]:


in_used = pd.merge(most_used, most_viewed, how="left", left_index=True, right_index=True)
in_viewed = pd.merge(most_used, most_viewed, how="right", left_index=True, right_index=True)


# 
# ### Relations Between Tags
# One way of trying to gauge how pairs of tags are related to each other, is to count how many times each pair appears together. Let's do this.
# 
# We'll begin by creating a list of all tags.

# In[42]:


all_tags = list(tag_count.index)


# We'll now create a dataframe where each row will represent a tag, and each column as well. Something like this:
# 
#  |**tag1**|**tag2**|**tag3**
# :-----:|:-----:|:-----:|:-----:
# tag1| | | 
# tag2| | | 
# tag3| | | 

# In[43]:


associations = pd.DataFrame(index=all_tags, columns=all_tags)
associations.iloc[0:4,0:4]


# 
# We will now fill this dataframe with zeroes and then, for each lists of tags in questions["Tags"], we will increment the intervening tags by one. The end result will be a dataframe that for each pair of tags, it tells us how many times they were used together.

# In[44]:


associations.fillna(0, inplace=True)

for tags in questions["Tags"]:
    associations.loc[tags, tags] += 1


# This dataframe is quite large. Let's focus our attention on the most used tags. We'll add some colors to make it easier to talk about the dataframe.

# In[45]:


relations_most_used = associations.loc[most_used.index, most_used.index]

def style_cells(x):
    helper_df = pd.DataFrame('', index=x.index, columns=x.columns)
    helper_df.loc["time-series", "r"] = "background-color: yellow"
    helper_df.loc["r", "time-series"] = "background-color: yellow"
    for k in range(helper_df.shape[0]):
        helper_df.iloc[k,k] = "color: blue"
    
    return helper_df

relations_most_used.style.apply(style_cells, axis=None)


# The cells highlighted in yellow tell us that time-series was used together with r 22 times. The values in blue tell us how many times each of the tags was used. We saw earlier that machine-learning was used 2693 times and we confirm it in this dataframe.
# 
# It's hard for a human to understand what is going on in this dataframe. Let's create a heatmap. But before we do it, let's get rid of the values in blue, otherwise the colors will be too skewed.

# In[46]:


for i in range(relations_most_used.shape[0]):
    relations_most_used.iloc[i,i] = pd.np.NaN


# In[47]:



plt.figure(figsize=(12,8))
sns.heatmap(relations_most_used, cmap="Greens", annot=False)


# The most used tags also seem to have the strongest relationships, as given by the dark concentration in the bottom right corner. However, this could simply be because each of these tags is used a lot, and so end up being used together a lot without possibly even having any strong relation between them.
# 
# A more intuitive manifestation of this phenomenon is the following. A lot of people buy bread, a lot of people buy toilet paper, so they end up being purchased together a lot, but purchasing one of them doesn't increase the chances of purchasing the other.
# 
# Another shortcoming of this attempt is that it only looks at relations between pairs of tags and not between multiple groups of tags. For example, it could be the case that when used together, dataset and scikit-learn have a "strong" relation to pandas, but each by itself doesn't.
# 
# So how do we attack both these problems? There is a powerful data mining technique that allows us to handle this: [association rules](https://en.wikipedia.org/wiki/Association_rule_learning). Association rules allow us to analytically spot relations like "people who purchase milk, also purchase eggs". Moreover, we can also measure how strong this relations are on several fronts: how common the relation is, how strong it is, and how independent the components of the relationship are (toilet paper and bread are probably more independent than eggs and milk — you'll learn more about [statistical independence](https://en.wikipedia.org/wiki/Independence_(probability_theory)) in the next step).
# 
# We won't get into the details of it, as the technique is out of scope for this course, but it is a path worth investigating!
# 
# ### Enter Domain Knowledge
# [Keras](https://keras.io/), [scikit-learn](https://scikit-learn.org/stable/), [TensorFlow](https://www.tensorflow.org/) are all Python libraries that allow their users to employ deep learning (a type of neural network).
# 
# Most of the top tags are all intimately related with one central machine learning theme: deep learning. If we want to be very specific, we can suggest the creation of Python content that uses deep learning for classification problems (and other variations of this suggestion).
# 
# At the glance of an eye, someone with sufficient domain knowledge can tell that the most popular topic at the moment, as shown by our analysis, is deep learning.
# 
# ### Just a Fad?
# Before we officially make our recommendation, it would be nice to solidy our findings with additional proof. More specifically, one thing that comes to mind is "Is deep learning just a fad?" Ideally, the content we decide to create will be the most useful for as long as possible. Could interest in deep learning be slowing down? Back to SEDE!
# 
# The file __all_questions.csv__ holds the result of the query below — this query fetches all of the questions ever asked on DSSE, their dates and tags.
# 
# __SELECT Id, CreationDate, Tags
#   FROM posts
#  WHERE PostTypeId = 1;
#  
# In this we will track the interest in deep learning across time. We will:
# 
# Count how many deep learning questions are asked per time period.
# The total amount of questions per time period.
# How many deep learning questions there are relative to the total amount of questions per time period.
# 
# 
# Let's read in the file into a dataframe called __all_questions.csv__. We'll parse the dates at read-time.

# In[48]:



all_q = pd.read_csv("all_questions.csv", parse_dates=["CreationDate"])


# 
# We can use the same technique as before to clean the tags column.

# In[49]:


all_q["Tags"] = all_q["Tags"].str.replace("^<|>$", "").str.split("><")


# 
# Before deciding which questions should be classified as being deep learning questions, we should decide what tags are deep learning tags.
# 
# The definition of what constitutes a deep learning tag we'll use is: a tag that belongs to the list ["lstm", "cnn", "scikit-learn", "tensorflow", "keras", "neural-network", "deep-learning"].
# 
# This list was obtained by looking at all the tags in most_used and seeing which ones had any relation to deep learning. You can use Google and read the tags descriptions to reach similar results.
# 
# We'll now create a function that assigns 1 to deep learning questions and 0 otherwise; and we use it.

# In[50]:


def class_deep_learning(tags):
    for tag in tags:
        if tag in ["lstm", "cnn", "scikit-learn", "tensorflow",
                   "keras", "neural-network", "deep-learning"]:
            return 1
    return 0


# In[51]:


all_q["DeepLearning"] = all_q["Tags"].apply(class_deep_learning)

all_q.sample(5)


# Looks good!
# 
# The data-science-techonology landscape isn't something as dynamic to merit daily, weekly, or even monthly tracking. Let's track it quarterly.
# 
# Since we don't have all the data for the first quarter of 2020, we'll get rid of those dates:

# In[52]:



all_q = all_q[all_q["CreationDate"].dt.year < 2020]


# Let's create a column that identifies the quarter in which a question was asked.

# In[54]:



def fetch_quarter(datetime):
    year = str(datetime.year)[-2:]
    quarter = str(((datetime.month-1) // 3) + 1)
    return "{y}Q{q}".format(y=year, q=quarter)

all_q["Quarter"] = all_q["CreationDate"].apply(fetch_quarter)


# In[55]:


all_q.head()


# For the final stretch of this screen, we'll group by quarter and:
# 
# Count the number of deep learning questions.
# Count the total number of questions.
# Compute the ratio between the two numbers above.

# In[56]:


quarterly = all_q.groupby('Quarter').agg({"DeepLearning": ['sum', 'size']})
quarterly.columns = ['DeepLearningQuestions', 'TotalQuestions']
quarterly["DeepLearningRate"] = quarterly["DeepLearningQuestions"]                                /quarterly["TotalQuestions"]
# The following is done to help with visualizations later.
quarterly.reset_index(inplace=True)
quarterly.sample(5)


# In[57]:


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


# 
# It seems that deep learning questions was a high-growth trend since the start of DSSE and it looks like it is plateauing. There is no evidence to suggest that interest in deep learning is decreasing and so we maintain our previous idea of proposing that we create deep learning content.
# 
# Here are some things to consider:
# 
# - What other content can we recommend that isn't as popular? You can try using association rules to find strong relations between tags.
# - What other popularity features could we include in our analysis? Perhaps scores and favourite counts?
# - We focused on other DSSE. How could we use other related sites to help us with our goal?
# - How can we leverage other sites to determine what non-data-science content to write about? For example, is there some mathematical field that leads to more questions than others?
# 
