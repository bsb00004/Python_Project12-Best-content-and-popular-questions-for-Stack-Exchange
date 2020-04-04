# Python_Project12-Best-content-popular-questions-for-Stack-Exchange
Task is to figuring out what is best content to write about on Stack Exchange.

{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Popular Data Science Questions¶\n",
    "The Goal this project is to use Data Science Stack Exchange to determine what content should a [data science](https://datascience.stackexchange.com/) education company create, based on interest by subject.\n",
    "\n",
    
    "### Stack Exchange\n",
    "Stack Exchange hosts sites on a multitude of fields and subjects, including mathematics, physics, philosophy, and [data science!](https://datascience.stackexchange.com/) Here's a sample of the most popular sites:\n",
    "<img src=\"https://dq-content.s3.amazonaws.com/469/se_sites.png\">\n",
    "[__Stack Exchange__](https://stackexchange.com/sites?view=list#percentanswered)\n",
    "\n",
    "If you open the link shared above, you'll find a complete list of Stack Exchange websites sorted by percentage of questions that received answers. At the time of this writing, Data Science Stack Exchange (DSSE) is on the bottom 10 sites with respect to this metric.\n",
    "\n",
    "The fact that DSSE is a data science dedicated site (contrarily to the others), coupled with it having a lot of an unanswered questions, makes it an ideal candidate for this investigation. DSSE will be the focus of this project.\n",
    "\n",
    "##### What kind of questions are welcome on this site?\n",
    "On DSSE's help center's section on questions , we can read that we should:\n",
    "\n",
    "- Avoid subjective questions.\n",
    "- Ask practical questions about Data Science — there are adequate sites for theoretical questions.\n",
    "- Ask specific questions.\n",
    "- Make questions relevant to others.\n",
    "\n",
    "All of these characteristics, if employed, should be helpful attributes to our goal.\n",
    "\n",
    "In the help center we also learned that in addition to the sites mentioned in the Learn section, there are other two sites that are relevant:\n",
    "\n",
    "- [Open Data](https://opendata.stackexchange.com/) (Dataset requests)\n",
    "- [Computational Science](https://scicomp.stackexchange.com/) (Software packages and algorithms in applied mathematics)\n",
    "\n",
    "##### What, other than questions, does DSSE's home subdivide into?\n",
    "On the home page we can see that we have four sections:\n",
    "\n",
    "- [Questions](https://datascience.stackexchange.com/questions) — a list of all questions asked;\n",
    "- [Tags](https://datascience.stackexchange.com/tags) — a list of tags (keywords or labels that categorize questions);\n",
    "\n",
    
    "<img src=\"https://camo.githubusercontent.com/46d9d26dbb54bbfaf2b92b100ec4c5e427708bf2/68747470733a2f2f64712d636f6e74656e742e73332e616d617a6f6e6177732e636f6d2f3436392f746167735f64732e706e67\">\n",
    "\n",
    
    "- [Users](https://datascience.stackexchange.com/users) — a list of users;\n",
    "- [Unanswered](https://datascience.stackexchange.com/unanswered) — a list of unanswered questions;\n",
    "The tagging system used by Stack Exchange looks just like what we need to solve this problem as it allow us to quantify how many questions are asked about each subject.\n",
    "\n",
    "Something else we can learn from exploring the help center, is that Stack Exchange's sites are heavily moderated by the community; this gives us some confidence in using the tagging system to derive conclusions.\n",
    "\n",
    "##### What information is available in each post?\n",
    "Looking, just as an example, at [this](https://datascience.stackexchange.com/questions/19141/linear-model-to-generate-probability-of-each-possible-output?rq=1) question, some of the information we see is:\n",
    "\n",
    "- For both questions and answers:\n",
    "    - The posts's score;\n",
    "    - The posts's title;\n",
    "    - The posts's author;\n",
    "    - The posts's body;\n",
    "- For questions only:\n",
    "    - How many users have it on their \"\n",
    "    - The last time the question as active;\n",
    "    - How many times the question was viewed;\n",
    "    - Related questions;\n",
    "    - The question's tags;\n",
    "\n",
    "### Stack Exchange Data Explorer\n",
    "Perusing the table names, a few stand out as relevant for our goal:\n",
    "\n",
    "- Posts\n",
    "- PostTags\n",
    "- Tags\n",
    "- TagSynonyms\n",
    "\n",
    "Running a few exploratory queries, leads us to focus our efforts on Posts table.\n",
    "<img src=\"https://dq-content.s3.amazonaws.com/469/PostTypes.png\">\n",
    "\n",
    "For examples, the Tags table looked very promising as it tells us how many times each tag was used, but there's no way to tell just from this if the interest in these tags is recent or a thing from the past.\n",
    "\n",
    "Note that with the exception of the tags column, the last few columns contain information about how popular the post is — the kind of information we're after.\n",
    "\n",
    "| Id  | TagName          | Count | ExcerptPostId | WikiPostId |\n",
    "|-----|------------------|-------|---------------|------------|\n",
    "| 2   | machine-learning | 6919  | 4909          | 4908       |\n",
    "| 46  | python           | 3907  | 5523          | 5522       |\n",
    "| 81  | neural-network   | 2923  | 8885          | 8884       |\n",
    "| 194 | deep-learning    | 2786  | 8956          | 8955       |\n",
    "| 77  | classification   | 1899  | 4911          | 4910       |\n",
    "| 324 | keras            | 1736  | 9251          | 9250       |\n",
    "| 128 | scikit-learn     | 1303  | 5896          | 5895       |\n",
    "| 321 | tensorflow       | 1224  | 9183          | 9182       |\n",
    "| 47  | nlp              | 1162  | 147           | 146        |\n",
    "| 24  | r                | 1114  | 49            | 48         |\n",
    "\n",
    "Since we're only interested in recent posts, we'll limit our analysis to the posts of 2019. (At the time of writing it is early 2020).\n",
    "\n",
    "The dataset we'll be using in this project is __2019_questions.csv__, is the one resulting from Running a query against the SEDE DSSE database that extracts the columns listed above for all the questions in 2019 .\n",
    "\n",
    "### Getting the Data\n",
    "To get the relevant data we run the following query.\n",
    "\n",
    "SELECT Id, CreationDate,\n",
    "  Score, ViewCount, Tags,\n",
    "  AnswerCount, FavoriteCount\n",
    "  FROM posts\n",
    "  WHERE PostTypeId = 1 AND YEAR(CreationDate) = 2019;\n",
    " \n",
    "Here's what the first few rows look like:\n",
    "\n",
    "\n",
    "| Id    | PostTypeId | CreationDate        | Score | ViewCount | Tags                                                              | AnswerCount | FavoriteCount |\n",
    "|-------|------------|---------------------|-------|-----------|-------------------------------------------------------------------|-------------|---------------|\n",
    "| 44419 | 1          | 2019-01-23 09:21:13 | 1     | 21        | < machine-learning>< data-mining>                                   | 0           |               |\n",
    "| 44420 | 1          | 2019-01-23 09:34:01 | 0     | 25        | < machine-learning>< regression>< linear-regression>< regularization> | 0           |               |\n",
    "| 44423 | 1          | 2019-01-23 09:58:41 | 2     | 1651      | < python>< time-series>< forecast>< forecasting>                      | 0           |               |\n",
    "| 44427 | 1          | 2019-01-23 10:57:09 | 0     | 55        | < machine-learning>< scikit-learn>< pca>                             | 1           |               |\n",
    "| 44428 | 1          | 2019-01-23 11:02:15 | 0     | 19        | < dataset>< bigdata>< data>< speech-to-text>                          | 0           |               |"
   ]
  },
