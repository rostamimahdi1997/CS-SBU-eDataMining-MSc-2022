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
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.datasets import fetch_openml
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

from google.colab import drive
drive.mount('/gdrive')

! ls /gdrive/MyDrive/csv

root = '/gdrive/MyDrive/csv/'
data= pd.read_csv(root + 'train.csv')
data.head()

data.info()

data['price_range'].head()

data_1 = data.iloc[: , :-1 ]
data_2 = data.iloc[ : , -1]
print(data_1)
print(data_2)

import pandas as pd
import statsmodels.api as sm


def forward_regression(X, y,
                       threshold_in = 0.01,
                       verbose =False):
    initial_list = []
    included = list(initial_list)
    while True:
        changed=False
        excluded = list(set(X.columns)-set(included))
        new_pval = pd.Series(index=excluded)
        for new_column in excluded:
            model = sm.OLS(y, sm.add_constant(pd.DataFrame(X[included+[new_column]]))).fit()
            new_pval[new_column] = model.pvalues[new_column]
        best_pval = new_pval.min()
        if best_pval < threshold_in:
            best_feature = new_pval.idxmin()
            included.append(best_feature)
            changed=True
            if verbose:
                print('Add  {:30} with p-value {:.6}'.format(best_feature, best_pval))

        if not changed:
            break

    return included

data_forward = forward_regression(data_1, data_2)
print(data_forward)

data.drop(columns=['blue','clock_speed','dual_sim','fc','four_g','int_memory','m_dep','n_cores','sc_h','sc_w','talk_time','three_g','touch_screen','wifi' , 'pc'] , inplace= True)

data.head()

X = data.iloc[: , :-1].values
y = data.iloc[: , -1].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)
print(X_train)
print(y_train)
print(X_test) 
print(y_test)

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
print(X_train) 
# print(X_test)

classifier = LogisticRegression(random_state = 0)
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)
print(np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1))

cm = confusion_matrix(y_test, y_pred)
print(cm)
print(accuracy_score(y_test, y_pred))

pick_pca = data_1.values 
pick_pca2 = data_2.values
standard = StandardScaler().fit_transform(pick_pca)
# print(pick_pca)
# print(pick_pca2)

pca = PCA(n_components=5)
principalComponents = pca.fit_transform(standard)
principalDf = pd.DataFrame(data = principalComponents
             , columns = ['principal component 1', 'principal component 2','principal component 3','principal component 4','principal component 5'])

finalDf = pd.concat([principalDf, data['price_range']], axis = 1)
# print(finalDf)
finalDf.head()

pca.explained_variance_ratio_

xPca  = finalDf.iloc[: , :-1]
yPca = finalDf.iloc[ : , -1]
# print(xPca)
print(yPca)
X_trainPca, X_testPca, y_trainPca, y_testPca = train_test_split(xPca, yPca, test_size = 0.2, random_state = 0)

scaler = StandardScaler()
scaler.fit(X_trainPca)
X_testPca = scaler.transform(X_testPca)
X_trainPca = scaler.transform(X_trainPca)

pca = PCA(.95)

pca.fit(X_trainPca)

X_trainPca = pca.transform(X_trainPca)
X_testPca = pca.transform(X_testPca)
print(X_trainPca)

min_value = data['battery_power'].min()
max_value = data['battery_power'].max()
print(min_value)
print(max_value)

bins = np.linspace(min_value,max_value,4)
print(bins)

labels = ['small', 'medium', 'big']

data['bins'] = pd.cut(data['battery_power'], bins=bins, labels=labels, include_lowest=True)
print(data['bins'])

data.head()

# X_HOT = data.iloc[:, :-1].values
# Y_HOT = data.iloc[: , -1].values
# print(Y_HOT)
# ct = ColumnTransformer(transformers=[("encoder" , OneHotEncoder() , [0])] , remainder="passthrough")
# Y_HOT= np.array(ct.fit_transform(Y_HOT))
# # print(data_2)
df_new = pd.get_dummies(data,columns=['price_range'] ,prefix='range')
print(df_new)

X_logis = data.iloc[: , ]
print(X_logis)