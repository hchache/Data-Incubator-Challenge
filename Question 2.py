
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy.stats import chisquare
from scipy import stats
from sklearn import linear_model
pd.options.display.float_format = '{:,.10f}'.format


# In[2]:


# Read input CSV file - Montana
df_mt = pd.read_csv("MT-clean.csv", low_memory=False)
# df_mt.head()


# In[3]:


# Read input CSV file - Vermont
df_vt = pd.read_csv("VT-clean.csv", low_memory=False)
# df_vt.head()


# #### What proportion of traffic stops in Montana involved male drivers? In other words, divide the number of traffic stops involving male drivers by the total number of stops.

# In[4]:


male_prop, female_prop = df_mt.driver_gender.value_counts()/df_mt.driver_gender.count()
print("proportion of traffic stops in Montana involved male drivers: ",male_prop)


# #### How many more times likely are you to be arrested in Montana during a traffic stop if you have out of state plates?

# In[5]:


out_of_state_false, out_of_state_true = df_mt.out_of_state.value_counts()/df_mt.out_of_state.count()
print("if you have out of state plates, you are ",out_of_state_true/out_of_state_false, 
      " times more likely to be arrested in Montana during a traffic stop")


# In[6]:


m = df_mt.is_arrested.value_counts()/df_mt.is_arrested.count()


# In[7]:


v = df_vt.is_arrested.value_counts()/df_vt.is_arrested.count()


# #### Perform a (χ2) test to determine whether the proportions of arrests in these two populations are equal. What is the value of the test statistic?
# 
# |  | Arrested  | Not Arrested |
# |------|------|------|
# |   MT  | 17195|   807923  |
# |   VT  | 3331|   279954  |
# 

# In[8]:


chi_squared_stat = (((m-v)**2)/v).sum()
print(chi_squared_stat)


# In[9]:


observed = np.array(m)
expected = np.array(v)
chisquare_value, pvalue = chisquare(observed, expected)


# In[10]:


print("value of the test statistic: ",chisquare_value)


# #### What proportion of traffic stops in Montana resulted in speeding violations? In other words, find the number of violations that include "Speeding" in the violation description and divide that number by the total number of stops (or rows in the Montana dataset).

# In[11]:


print("proportion of traffic stops in Montana resulted in speeding violations: ",
      df_mt.violation.value_counts()['Speeding']/df_mt.violation.count())


# #### How much more likely does a traffic stop in Montana result in a DUI than a traffic stop in Vermont? To compute the proportion of traffic stops that result in a DUI, divide the number of stops with "DUI" in the violation description by the total number of stops.

# In[12]:


m_DUI = (df_mt['violation'].str.contains("DUI") == True).sum()/df_mt.violation.count()


# In[13]:


v_DUI = (df_vt['violation'].str.contains("DUI") == True).sum()/df_vt.violation.count()


# In[14]:


print("a traffic stop in Montana result in a DUI than a traffic stop in Vermont: ",m_DUI/v_DUI)


# #### What is the extrapolated, average manufacture year of vehicles involved in traffic stops in Montana in 2020? To answer this question, calculate the average vehicle manufacture year for each year's traffic stops. Extrapolate using a linear regression.

# In[15]:


# Assign previous value to NaN in column stop_date
df_mt_ext = df_mt
stop_date_col= df_mt_ext['stop_date']
is_stop_date_null = stop_date_col.isnull()
stop_date_null_true = stop_date_col[is_stop_date_null]
a = int(stop_date_null_true.index[0])
df_mt_ext['stop_date'].fillna(df_mt_ext['stop_date'][a-1], inplace = True)


# In[16]:


df_mt_ext["stop_date"] = pd.to_datetime(df_mt_ext["stop_date"])
df_mt_ext["stop_year"] = df_mt_ext['stop_date'].dt.year


# In[17]:


# Remove all rows which contains vehicle year as UNK, NON and NaN
df_mt_ext['vehicle_year'].fillna('0', inplace = True)
a = df_mt_ext['vehicle_year'].isin(['UNK','NON-','0'])
b = df_mt_ext[a]
c = b.index
df_mt_ext = df_mt_ext.drop(c)


# In[18]:


# Groupby stopyear and calculate mean vehicle year
df_mt_ext['vehicle_year'] = df_mt_ext['vehicle_year'].astype(int)
ab = df_mt_ext.groupby('stop_year')['vehicle_year'].mean().reset_index()


# In[19]:


# Using interpolate
x = ab['stop_year']
y = ab['vehicle_year']
f = interpolate.interp1d(x, y,kind='linear', fill_value='extrapolate', bounds_error=False)
xnew = int(2020)
# Answer
y_predicted_interpolate = float(f(xnew))
print("Using interpolate - the average vehicle manufacture year: ",y_predicted_interpolate)


# In[20]:


# Using stats.linregress
slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
# Answer
y_predicted_stats = 2020*slope + intercept
print("Using Stats - the average vehicle manufacture year: ",y_predicted_stats)
# Answer tot next question
print("the p-value of this linear regression: ",p_value)


# In[21]:


regr = linear_model.LinearRegression()
x_train = x.values.reshape((-1, 1))
y_train = y.values.reshape((-1, 1))

regr.fit(x_train, y_train)

xnew1  = [2020]
xnew1 = np.reshape(xnew1, (-1, 1))
ynew1 = regr.predict(xnew1)

print("Using sklearn linear model - the average vehicle manufacture year: ",ynew1)


# #### Combining both the Vermont and Montana datasets, find the hours when the most and least number of traffic stops occurred. What is the difference in the total number of stops that occurred in these two hours? Hours range from 00 to 23. Round stop times down to compute this difference.

# In[23]:


# Merge two datasets
df_mt_merge = pd.read_csv("MT-clean.csv", low_memory=False)
df_merged = pd.merge(df_mt_merge, df_vt, how='outer', suffixes=('_mt', '_vt'))


# In[24]:


df_merged['stop_hour'] = df_merged.stop_time.str[:2]
stop_hours = df_merged['stop_hour'].value_counts()
print("Difference in the total number of stops that occurred in these two hours: ",
      stop_hours[0] - stop_hours[len(stop_hours)-1])


# #### We can use the traffic stop locations to estimate the areas of the counties in Montana. Represent each county as an ellipse with semi-axes given by a single standard deviation of the longitude and latitude of stops within that county. What is the area, in square kilometers, of the largest county measured in this manner? Please ignore unrealistic latitude and longitude coordinates

# In[25]:


df_area = df_mt[['id','county_name','lat','lon']]

# id             825118
# county_name    821062
# lat            824682
# lon            824682
# Filling the county name would cost unnecessary computational power. 
# by deleting NaN records in county column, we are loosing 0.4% Data

county_col= df_area['county_name']
is_county_col_null = county_col.isnull()
county_col_null_true = county_col[is_county_col_null]
df_area = df_area.drop(county_col_null_true.index)


# In[26]:


df_area_std = df_area.groupby('county_name')['lat','lon'].std().reset_index()


# In[27]:


import math
# Considering each lan degree equals to 111.321 kilometers
lat_in_km = (df_area_std['lat'] * math.pi / 180)* 111.321
lon_in_km = (df_area_std['lon'] * math.pi / 180) * 111.321
df_area_std['area'] = math.pi * lat_in_km * lon_in_km


# In[28]:


print("Area of the largest county: ",df_area_std['area'].max())
