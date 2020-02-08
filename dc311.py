#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


data = pd.read_csv('https://opendata.arcgis.com/datasets/98b7406def094fa59838f14beb1b8c81_10.csv')


# In[3]:


data.head()


# In[8]:


date_cols = ['ADDDATE', 'RESOLUTIONDATE', 'SERVICEDUEDATE', 'SERVICEORDERDATE', 'INSPECTIONDATE']


# In[9]:


data.info()


# In[10]:


data[date_cols] = data[date_cols].apply(pd.to_datetime)


# In[11]:


data.SERVICECODEDESCRIPTION.value_counts().head(20)


# In[12]:


oos = data[data.SERVICECODEDESCRIPTION == 'Out of State Parking Violation (ROSA)']


# In[14]:


oos.info()


# In[15]:


oos.STATUS_CODE.value_counts()


# In[16]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[17]:


oos.plot(x ='LATITUDE', y='LONGITUDE', kind = 'scatter')


# In[19]:


import seaborn as sns
sns.set(rc ={'figure.figsize': (14,8)})


# In[20]:


sns.scatterplot(x= 'LATITUDE', y= 'LONGITUDE',
               hue='WARD', data = oos,
               palette= sns.color_palette("Set1", 8))


# In[25]:


oos.ADDDATE.dt.hour.value_counts().sort_index().plot.bar()


# In[26]:


def plot_value_counts(ser):
    ser.value_counts().sort_index().plot.bar()


# In[27]:


plot_value_counts(oos.SERVICEDUEDATE.dt.day)


# In[30]:


plot_value_counts(oos.RESOLUTIONDATE.dt.hour)


# In[31]:


graf = data[data.SERVICECODEDESCRIPTION == 'Graffiti Removal']


# In[32]:


graf


# In[33]:


graf.WARD.value_counts()


# In[37]:


graf.plot(x="LATITUDE", y="LONGITUDE", kind="scatter")


# In[38]:


sns.scatterplot(x="LONGITUDE", y="LATITUDE", hue="WARD", data=graf, palette=sns.color_palette("Set1", 8))


# In[40]:


plot_value_counts(graf.ADDDATE.dt.hour)


# In[41]:


plot_value_counts(graf.ADDDATE.dt.day)


# In[45]:


plot_value_counts(graf.RESOLUTIONDATE.dt.month)


# In[46]:


data.info()


# In[48]:


bulk_df = data[data.SERVICECODEDESCRIPTION == 'Bulk Collection']


# In[53]:


bulk_df = bulk_df[['SERVICECALLCOUNT', 'ADDDATE']].set_index('ADDDATE')


# In[54]:


bulk_df


# In[56]:


grouped_df = bulk_df.resample('1w').sum()


# In[57]:


grouped_df = grouped_df.reset_index()


# In[58]:


grouped_df = grouped_df.reset_index()


# In[61]:


grouped_df.columns = ['Week Number', 'Date', 'Call Count']
grouped_df.head()


# In[62]:


from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression


# In[64]:


model = PolynomialFeatures(degree=2)
xp = model.fit_transform(grouped_df[['Week Number']])
lm = LinearRegression()
lm.fit(xp, grouped_df['Call Count'])


# In[66]:


grouped_df['predictions']= lm.predict(xp)
grouped_df.head()


# In[67]:


import seaborn as sns
sns.scatterplot(x='Week Number',
                y='Call Count',
                data = grouped_df)
sns.lineplot(x='Week Number',
            y='predictions', 
            data=grouped_df)
plt.ylabel('Call Count')
plt.title("Predicting Call Count by Week");


# In[ ]:




