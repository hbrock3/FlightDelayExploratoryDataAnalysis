#!/usr/bin/env python
# coding: utf-8

# This report summarizes a EDA done on the provided domestic flight delay data for January 2020. This data set categorizes a flight departure as late if it is delayed by more than 15 minutes.

# First, the data set will be loaded into Jupyter and the head of the data frame will be printed out to confirm proper lading of the CSV file.

# In[1]:


import pandas as pd

df = pd.read_csv('train_test_small.csv')
df.head()


# Next, group the data by airline carrier. Print out the first tuple for each carrier to verify the groups were created properly.

# In[2]:


carriers = df.groupby('CARRIER_NAME')
carriers.first()


# Now that we have the data grouped by carrier, we can determine the 5 most and 5 least relable airlines for on-time departure.

# In[3]:


def mostReliable(deps, attr):
    print('Here are the 5 most reliable ' + attr + ':\n')
    print('{:4s}  {:30s}{:15s}'.format('Rank', attr, 'Percent on-time'))
    keys = deps.keys()
    for i in range(5):
        print('{:4d}. {:30s}{:4.1f}%'.format(i + 1, keys[i], deps[i] * 100.))

departure_ratios = (1. - carriers['DEP_DEL15'].sum() / carriers['DEP_DEL15'].count()).sort_values(ascending=False)
mostReliable(departure_ratios, 'airlines')


# In[4]:


def leastReliable(deps, attr):
    print('Here are the 5 least reliable ' + attr + ':\n')
    print('{:4s}  {:30s}{:15s}'.format('Rank', attr, 'Percent on-time'))
    keys = deps.keys()
    for i in range(deps.count() - 1, deps.count() - 6, -1):
        print('{:4d}. {:30s}{:4.1f}%'.format(i + 1, keys[i], deps[i] * 100.))

leastReliable(departure_ratios, 'airlines')


# Next, we want to do a similar comparison, but for the departure airports.

# In[5]:


airports = df.groupby('DEPARTING_AIRPORT')
airports.first()


# In[6]:


departure_ratios = (1. - airports['DEP_DEL15'].sum() / airports['DEP_DEL15'].count()).sort_values(ascending=False)
mostReliable(departure_ratios, 'airports')


# In[7]:


leastReliable(departure_ratios, 'airports')


# In[8]:


correlations = df.corr()['DEP_DEL15'].abs().sort_values(ascending=False)
print(correlations)


# In[9]:


print('The most correlated column to the departurs delays is', correlations.keys()[1] + '.')


# In[30]:


get_ipython().run_line_magic('matplotlib', 'inline')

import matplotlib.pyplot as plt

fig, ax =  plt.subplots(3, 1, figsize=(4,12))
keys = departure_ratios.keys()
departure_counts = airports['DEP_DEL15'].sum()
flight_totals = airports['DEP_DEL15'].count()

# Left plot
ax[0].set_ylim(0.85, 0.95)
ax[0].set_title('Most Reliable Airports Showing On-time Departure Ratios')
ax[0].set_xlabel('Airports')
ax[0].set_ylabel('Ratio on-time')
ax[0].grid(axis='y', linestyle = "-.")
ax[0].set_xticklabels(keys[0:5], rotation = 90)
ax[0].bar(keys[0:5], departure_ratios[0:5])

# Left plot
# ax[1].set_ylim(0.85, 0.95)
ax[1].set_title('Most Reliable Airports Showing Actual Delay Counts')
ax[1].set_xlabel('Airports')
ax[1].set_ylabel('Delay Counts')
ax[1].grid(axis='y', linestyle = "-.")
ax[1].set_xticklabels(keys[0:5], rotation = 90)
ax[1].bar(keys[0:5], departure_counts[keys[0:5]])

ax[2].set_title('Most Reliable Airports Showing Actual Flight Counts')
ax[2].set_xlabel('Airports')
ax[2].set_ylabel('# Flights')
ax[2].grid(axis='y', linestyle = "-.")
ax[2].set_xticklabels(keys[0:5], rotation = 90)
ax[2].bar(keys[0:5], flight_totals[keys[0:5]])

fig.tight_layout()
plt.show()


# In[1]:


fig, ax =  plt.subplots()
ax.set_title('Data Pairs for DEP_DEL15 and ' + correlations.keys()[1])
ax.set_xlabel('DEP_DEL15')
ax.set_ylabel(correlations.keys()[1])
plt.xticks((0, 1), ('On Time', 'Delayed'))
ax.scatter(df['DEP_DEL15'], df[correlations.keys()[1]])
plt.show()


# In[ ]:




