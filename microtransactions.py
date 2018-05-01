
# coding: utf-8

# # Project: Hypothesis Testing for Microtransactions
# Brian is a Product Manager at FarmBurg, a company that makes a farming simulation social network game.  In the FarmBurg game, you can plow, plant, and harvest different crops.
# 
# Today, you will be acting as Brian's data analyst for an A/B Test that he has been conducting.

# ## Part 1: Testing for Significant Difference

# Start by importing the following modules that you'll need for this project:
# - `pandas` as `pd`

# In[81]:

import pandas as pd
import re, numpy
import scipy.stats


# Brian tells you that he ran an A/B test with three different groups: A, B, and C.  You're kind of busy today, so you don't ask too many questions about the differences between A, B, and C.  Maybe they were shown three different versions of an ad.  Who cares?
# 
# (HINT: you will care later)
# 
# Brian gives you a CSV of results called `clicks.csv`.  It has the following columns:
# - `user_id`: a unique id for each visitor to the FarmBerg site
# - `ab_test_group`: either `A`, `B`, or `C` depending on which group the visitor was assigned to
# - `click_day`: only filled in *if* the user clicked on a link to purchase
# 
# Load `clicks.csv` into the variable `df`.

# In[28]:

df = pd.read_csv(filepath_or_buffer = './clicks.csv', header='infer')
# print type(str(df['click_day'])), str(df['click_day'])


# Define a new column called `is_purchase` which is `Purchase` if `click_day` is not `None` and `No Purchase` if `click_day` is `None`.  This will tell us if each visitor clicked on the Purchase link.

# In[57]:

def purchase_gen(click):
    if re.search(r"\w{4,}", str(click)):
        return "Purchase"
    else:
        return "No Purchase"
df['is_purchase'] = df.click_day.apply(purchase_gen)
# print df.head


# We want to count the number of users who made a purchase from each group.  Use `groupby` to count the number of `Purchase` and `No Purchase` from each `group`.  Save your answer to the variable `purchase_counts`.
# 
# **Hint**: Group by `group` and `is_purchase` and the function `count` on the column `user_id`.

# In[69]:

purchase_counts = df.groupby(['group', 'is_purchase']).size()
print purchase_counts


# This data is *categorical* and there are *more than 2* conditions, so we'll want to use a chi-squared test to see if there is a significant difference between the three conditions.
# 
# Start by filling in the contingency table below with the correct values:
# ```py
# contingency = [[groupA_purchases, groupA_not_purchases],
#                [groupB_purchases, groupB_not_purchases],
#                [groupC_purchases, groupC_not_purchases]]
# ```

# In[80]:

contingency = numpy.array([[purchase_counts[1], purchase_counts[0]], 
                          [purchase_counts[3], purchase_counts[2]], 
                          [purchase_counts[5], purchase_counts[4]]])
# print contingency


# Now import the function `chi2_contingency` from `scipy.stats` and perform the chi-squared test.
# 
# Recall that the *p-value* is the second output of `chi2_contingency`.

# In[86]:

chi2_result, p_value, dof, ex = scipy.stats.chi2_contingency(contingency) 
print p_value


# In[ ]:




# Great! It looks like a significantly greater portion of users from Group A made a purchase.

# ## Part 2: Testing for Exceeding a Goal
# 
# Your day is a little less busy than you expected, so you decide to ask Brian about his test.
# 
# **You**: Hey Brian! What was that test you were running anyway?
# 
# **Brian**: It was awesome! We are trying to get users to purchase a small FarmBurg upgrade package.  It's called a microtransaction.  We're not sure how much to charge for it, so we tested three different price points: \$0.99, \$1.99, and \$4.99.  It looks like significantly more people bought the upgrade package for \$0.99, so I guess that's what we'll charge.
# 
# **You**: Oh no! I should have asked you this before we did that chi-squared test.  I don't think that this was the right test at all.  It's true that more people wanted purchase the upgrade at \$0.99; you probably expected that.  What we really want to know is if each price point allows us to make enough money that we can exceed some target goal.  Brian, how much do you think it cost to build this feature?
# 
# **Brian**: Hmm.  I guess that we need to generate a minimum of $1000 per week in order to justify this project.
# 
# **You**: We have some work to do!

# How many visitors came to the site this week?
# 
# Hint: Look at the length of `df`.

# In[91]:

users_count = df.shape[0]
print users_count


# Let's assume that this is how many visitors we generally get each week.  Given that, calculate the percent of visitors who would need to purchase the upgrade package at each price point (\$0.99, \$1.99, \$4.99) in order to generate \$1000 per week.

# In[104]:

# Calculate the number of people who would need to purchase a $0.99 upgrade in order to generate $1000.
upgrade_99 = 1000 / 0.99
count_99 = upgrade_99 / 4998 * 100
print int(upgrade_99), count_99
# Then divide by the number of people who visit the site each week.


# In[105]:

# Calculate the number of people who would need to purchase a $1.99 upgrade in order to generate $1000.
upgrade_199 = 1000 / 1.99
count_199 = upgrade_199 / 4998 * 100
print int(upgrade_199), count_199
# Then divide by the number of people who visit the site each week.


# In[106]:

# Calculate the number of people who would need to purchase a $4.99 upgrade in order to generate $1000.
upgrade_499 = 1000 / 4.99
count_499 = upgrade_499 / 4998 * 100
print int(upgrade_499), count_499
# Then divide by the number of people who visit the site each week.


# Note that you need a smaller percentage of purchases for higher price points.
# 
# Now, for each group, perform a binomial test using `binom_test` from `scipy.stats`.
# - `x` will be the number of purchases for that group
# - `n` will be the total number of visitors assigned to that group
# - `p` will be the target percent of purchases for that price point (calculated above)
# 
# Recall that:
# - Group `A` is the \$0.99 price point
# - Group `B` is the \$1.99 price point
# - Group `C` is the \$4.99 price point

# In[107]:

# import the binomial test from scipy.stats here
N = 4998


# In[111]:

# Test group A here
X = contingency[0][0]
bi_groupA = scipy.stats.binom_test(X, N, 0.202); print bi_groupA


# In[112]:

# Test group B here
X = contingency[1][0]
bi_groupB = scipy.stats.binom_test(X, N, 0.105); print bi_groupB


# In[114]:

# Test group C here
X = contingency[2][0]
bi_groupC = scipy.stats.binom_test(X, N, 0.004); print bi_groupC


# If any of the groups passed the binomial test with $p < 0.05$, then we can be confident that enough people will buy the upgrade package at that price point to justify the feature.
# 
# Which price point should Brian go with?  Did this surprise you?
