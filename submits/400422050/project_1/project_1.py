# -*- coding: utf-8 -*-
"""amir.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1R7OP_jLCFji-CEcH1R_5QevPWJkc48lR

# New Section
"""

import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

from google.colab import drive
drive.mount('/gdrive')

#the main data is called "data"

root = '/gdrive/MyDrive/csv/'
pd.set_option('display.max_columns' , None)
data = pd.read_csv(root + 'csv_1.csv')
data.head()

data.info()

#here we delete columns with less than 50% null data
data.columns[(data.isna().sum())/len(data)>0.50]

#Now we need to shrink the range of data changes that are large
for cols in data.columns :
  if data[cols].dtype =='int64' or data[cols].dtype == 'float64':
    data[cols] =(data[cols] - data[cols].mean())/data[cols].std()

data.head()

#Now we need to delete the int or float null data
data.fillna(data._get_numeric_data().mean(),inplace = True)

data.isna().sum()


#Now we need to fill in the data that is typed str or obj and is null
for cols in data.columns :
  if data[cols].dtype == 'bool' or data[cols].dtype == 'object':
    data[cols].fillna(data[cols].value_counts().head(1).index[0],inplace=True)

data.isna().sum()

#Now we need to find and delete outlier data
for cols in data.columns:
  if data[cols].dtype == 'int64' or data[cols].dtype == 'float64' :
    upperRange = data[cols].mean()+3*data[cols].std()
    lowerRange = data[cols].mean() - 3 *data[cols].std()
    indexs = data[(data[cols]>upperRange) | (data[cols] < lowerRange)] .index
data2 =data.drop(indexs)
data2.shape


#Number of ads in each geographical area
fig = px.pie(data, names='neighbourhood_group', title='share in neighborhood')
fig.show()

#Check general price indica tors
data[['neighbourhood_group','price']].groupby(['neighbourhood_group'] , as_index = False).median().sort_values(by='price', ascending= False)

data['host_name'].value_counts()

#The connection between visits and the most popular places
review = data.sort_values('number_of_reviews',ascending=False)
top_reviewed = review.loc[:,['neighbourhood','number_of_reviews']][:20]
top_reviewed = top_reviewed.groupby('neighbourhood').mean().sort_values('number_of_reviews',ascending=False).reset_index()
fig4,ax3 = plt.subplots(figsize=(12,8))
sns.barplot(x=top_reviewed['neighbourhood'],y=top_reviewed['number_of_reviews'].values,color='yellowgreen',ax=ax3)
plt.plot(top_reviewed['number_of_reviews'], marker='o', color='red',linestyle='--')
plt.ylabel('Reviews', fontsize='15')
plt.xlabel('Location',fontsize='15')
plt.ylim((400,580))
plt.title('Most-Reviewed Rentals by location',fontsize='15')                                                                          
plt.show()
sns.set()
import numpy as np
upper_east = data[data['neighbourhood'] == 'Upper East Side']
ninetieth_percentile = np.quantile(upper_east['number_of_reviews'], 0.85)
upper_east = upper_east[upper_east['number_of_reviews'] >= ninetieth_percentile]
upper_east = upper_east.sort_values('price',ascending=True)
private_room = upper_east[upper_east['room_type'] == 'Private room'].reset_index()
entire_home = upper_east[upper_east['room_type'] == 'Entire home/apt'].reset_index()
shared_room = upper_east[upper_east['room_type'] == 'Shared room'].reset_index()
private_cheapest = private_room.loc[0,:].reset_index()
private_cheapest.rename(columns={'index':'data','0':'values'},inplace=True)
entire_cheapest = entire_home.loc[0,:].reset_index()
entire_cheapest.rename(columns={'index':'data','0':'values'},inplace=True)
