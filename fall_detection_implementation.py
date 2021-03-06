# -*- coding: utf-8 -*-
"""Fall_Detection_Implementation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1huAJa7NEOukt8LMw0dRhwGt2HDkcF4kt

Import libraries required to execute the code.
"""

import numpy as np
import pandas as pd 

import matplotlib.pyplot as plotAxis
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

from sklearn.model_selection import cross_val_score, StratifiedKFold, RandomizedSearchCV
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

"""Load data file from the below mentioned location."""

# Reading data from csv file
#df = pd.read_csv("C:/Users/jaish/Downloads/ResearchMethodology/Project/Final/falldetection.csv", sep=",")
df = pd.read_csv("/content/falldeteciton.csv", sep=",")
print(df.head(10))

# Describe the dataframe columns
# We will discard activity column as that is a nominal attribute
df.iloc[:,1:7].describe()

ACTIVITY_COUNT = df['ACTIVITY'].value_counts().sort_index()
print(ACTIVITY_COUNT)

"""Plot the Pie chart for all the activities.

"""

ACTIVITY_DICT = {0:'Standing', 1:'Walking', 2:'Sitting', 3:'Falling', 4:'Cramps', 5:'Running'}
ACTIVITY_KEYS = list(ACTIVITY_DICT.keys())
activities = list(ACTIVITY_DICT.values())
area = [ACTIVITY_COUNT[0], ACTIVITY_COUNT[1], ACTIVITY_COUNT[2], ACTIVITY_COUNT[3], ACTIVITY_COUNT[4], ACTIVITY_COUNT[5]]
explode = (0, 0, 0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

Figure1, Axes1 = plotAxis.subplots()
Axes1.pie(area, labels=activities, explode = explode, autopct='%1.1f%%', startangle = 90, counterclock=False, shadow=False)
Axes1.axis('equal')
plotAxis.show()

sns.set(style="darkgrid")
Axes = sns.countplot(y='ACTIVITY', data=df)
Axes.set_yticklabels(activities);

"""Created pivot_table"""

Column_Names = ['TIME','SL','EEG','BP','HR','CIRCLUATION']
Pivot_Table = df.pivot_table(Column_Names,
               ['ACTIVITY'], aggfunc='median')
print(Pivot_Table)

"""Created Correlation matrix to check the relationship between two varibales or features."""

# Correlation matrix
unstage = df.drop('ACTIVITY', axis=1)
Correlation = unstage.corr()
print(Correlation)
# Plot figsize
Figure, Axes = plotAxis.subplots(figsize=(15, 11))
# Generate Color Map
Map_Color = sns.diverging_palette(220, 10, as_cmap=True)
# Generate Heat Map, allow annotations and place floats in map
sns.heatmap(Correlation, cmap=Map_Color, annot=True, fmt=".2f")
Axes.set_xticklabels(
    Column_Names,
    rotation=45,
    horizontalalignment='right'
);
Axes.set_yticklabels(Column_Names);

# Correlation matrix
unstage = df.drop(['ACTIVITY','HR','CIRCLUATION'], axis=1)
Correlation = unstage.corr()
print(Correlation)
# Plot figsize
Figure, Axes = plotAxis.subplots(figsize=(8, 6))
# Generate Color Map
colormap = sns.diverging_palette(220, 10, as_cmap=True)
# Generate Heat Map, allow annotations and place floats in map
sns.heatmap(Correlation, cmap=colormap, annot=True, fmt=".2f")
Axes.set_xticklabels(
    ['TIME','SL','EEG','BP'],
    rotation=45,
    horizontalalignment='right'
);
Axes.set_yticklabels(['TIME','SL','EEG','BP']);

"""Removed outliers from dataset df"""

Quantile1 = df.quantile(0.25)
Quantile2 = df.quantile(0.75)
Quantile_Difference = Quantile2 - Quantile1
dataframe_out = df[~((df < (Quantile1 - 1.5 * Quantile_Difference)) |(df > (Quantile2 + 1.5 * Quantile_Difference))).any(axis=1)]
dataframe_out.shape

"""Created a new column called Decision. This column will contain the values of 0 = 'No Fall', 1 = 'Fall' using following rule: Activity Value : 3 --> Fall, else --> No Fall

"""

DECISION = []
for i in dataframe_out['ACTIVITY']:
    if i == 3:
        DECISION.append('1')
    else: 
        DECISION.append('0')
dataframe_out['DECISION'] = DECISION
print(dataframe_out.head(10))

dataframe_out['DECISION'].value_counts().sort_index()

"""Split the dataset into x and y

"""

X_Split = dataframe_out.iloc[:,1:7]
Y_Split = dataframe_out['DECISION']
print(X_Split.shape)
print(Y_Split.shape)

print(X_Split.head(10))

print(Y_Split.head(10))

"""1. Split dataset into train and test.
2. Also applied the standard scaling to get optimized result.
"""

X_Train, X_Test, Y_Train, Y_Test = train_test_split(X_Split, Y_Split, test_size=0.1, random_state=50)
SC = StandardScaler()
X_Train = SC.fit_transform(X_Train)
X_Test = SC.fit_transform(X_Test)

"""1. Perform K-Nearest Neighbors Classifier.
2. Print confusion matrix and accuracy score

"""

KNN = KNeighborsClassifier()
KNN.fit(X_Train,Y_Train)
KNN_Pred = KNN.predict(X_Test)
Confusion_Matrix = confusion_matrix(Y_Test, KNN_Pred)
Accuracy_Score = accuracy_score(Y_Test, KNN_Pred)
Classification_Report = classification_report(Y_Test, KNN_Pred) 
print(Confusion_Matrix)
print('Accuracy Score :', '%.2f' %Accuracy_Score)
print('Classification Report :')
print(Classification_Report)

"""1. Perform Random Forest Classifier.
2. Print confusion matrix and accuracy score.
"""

# Perform 
RF = RandomForestClassifier()
RF.fit(X_Train,Y_Train)
RF_Pred = RF.predict(X_Test)
Confusion_Matrix_RF = confusion_matrix(Y_Test, RF_Pred)
Accuracy_Score_RF = accuracy_score(Y_Test, RF_Pred)
Classification_Report_RF = classification_report(Y_Test, RF_Pred) 
print(Confusion_Matrix_RF)
print('Accuracy Score :', '%.2f' %Accuracy_Score_RF)
print('Classification Report :')
print(Classification_Report_RF)

"""1. Perform SVM Classifier.
2. Print confusion matrix and accuracy score.
"""

Svc = SVC()
Svc.fit(X_Train,Y_Train)
SVC_Pred = Svc.predict(X_Test)
Confusion_Matrix_SVC = confusion_matrix(Y_Test, SVC_Pred)
Accuracy_Score_SVC = accuracy_score(Y_Test, SVC_Pred)
Classification_Report_SVC = classification_report(Y_Test, SVC_Pred) 
print(Confusion_Matrix_SVC)
print('Accuracy Score :', '%.2f' %Accuracy_Score_SVC)
print('Classification Report :')
print(Classification_Report_SVC)

"""Declaring K-Fold Size = 10 to perfrom Cross validation"""

Score = cross_val_score(RF, X_Split, Y_Split, cv=10)
print(Score)
print('Mean accuracy :')
print('%.2f' %Score.mean())

"""K Fold Cross validation with KNN classifier"""

Score = cross_val_score(KNN, X_Split, Y_Split, cv=10)
print(Score)
print('Mean accuracy :')
print('%.2f' %Score.mean())

"""Set up Stratified K Fold Cross Validation with n_splits=10

"""

K_Fold = StratifiedKFold(n_splits=10, random_state=None)
K_Fold.get_n_splits(X_Split,Y_Split)

"""K Fold Cross validation with Random Forest classifier"""

ACCURACY = []

for IDX_Train, IDX_Test in K_Fold.split(X_Split, Y_Split):
    #print('Train :' , train_index, 'Test : ', test_index)
    X1_train, X1_test = X_Split.iloc[IDX_Train], X_Split.iloc[IDX_Test]
    y1_train, y1_test = Y_Split.iloc[IDX_Train], Y_Split.iloc[IDX_Test]
    
    RF.fit(X1_train, y1_train)
    Test_Prediction = RF.predict(X1_test)
    Accuracy_Score = accuracy_score(Test_Prediction, y1_test)
    ACCURACY.append(Accuracy_Score)
    
print(ACCURACY)
print('Mean accuracy :')
print('%.2f' %np.array(ACCURACY).mean())

"""K Fold Cross validation with K Nearest Neighbour classifier.





"""

ACCURACY_KNN = []

for IDX_Train, IDX_Test in K_Fold.split(X_Split, Y_Split):
    #print('Train :' , train_index, 'Test : ', test_index)
    X1_train, X1_test = X_Split.iloc[IDX_Train], X_Split.iloc[IDX_Test]
    y1_train, y1_test = Y_Split.iloc[IDX_Train], Y_Split.iloc[IDX_Test]
    
    KNN.fit(X1_train, y1_train)
    Test_Prediction = KNN.predict(X1_test)
    Accuracy_Score = accuracy_score(Test_Prediction, y1_test)
    ACCURACY_KNN.append(Accuracy_Score)
    
print(ACCURACY_KNN)
print('Mean accuracy :')
print('%.2f' %np.array(ACCURACY_KNN).mean())

"""K Fold Cross validation with Support Vector Machine."""

ACCURACY_SVC = []

for IDX_Train, IDX_Test in K_Fold.split(X_Split, Y_Split):
    X1_train, X1_test = X_Split.iloc[IDX_Train], X_Split.iloc[IDX_Test]
    y1_train, y1_test = Y_Split.iloc[IDX_Train], Y_Split.iloc[IDX_Test]
    
    Svc.fit(X1_train, y1_train)
    Test_Prediction = Svc.predict(X1_test)
    Accuracy_Score = accuracy_score(Test_Prediction, y1_test)
    ACCURACY_SVC.append(Accuracy_Score)
    
print(ACCURACY_SVC)
print('Mean accuracy :')
print('%.2f' %np.array(ACCURACY_SVC).mean())

"""FEATURE IMPORTANCE"""

import matplotlib.pyplot as plt

RF_Model = RandomForestClassifier(random_state=0)
RF_Model.fit(X_Split,Y_Split)

print(RF_Model.feature_importances_) 
Importances = pd.Series(RF_Model.feature_importances_, index=X_Split.columns)
Importances.nlargest(10).plot(kind='barh')
plt.show()

import pandas as pd

Std = np.std([tree.feature_importances_ for tree in RF_Model.estimators_], axis=0)
figure, axes = plt.subplots()
Importances.plot.bar(yerr=Std, ax=axes)
axes.set_title("Feature importances")
axes.set_ylabel("Mean decrease in impurity")
figure.tight_layout()

"""FORWARD FEATURE SELECTION"""

# Importing the necessary libraries
from mlxtend.feature_selection import SequentialFeatureSelector as SFS

# Sequential Forward Selection
sfs = SFS(RandomForestClassifier(),
          k_features=4,
          forward=True,
          floating=False,
          scoring = 'accuracy',
          cv = 0)

sfs.fit(X_Split, Y_Split)
sfs.k_feature_names_

"""FORWARD FEATURE SELECTION WITH n FEATURES"""

# Reading data from csv file
df1 = pd.read_csv("C:/Users/jaish/Downloads/ResearchMethodology/Project/Final/falldetection.csv", sep=",")
print(df1.head(10))

dataframe_1=df1.drop(columns=['HR','CIRCLUATION'])

dataframe_1

Quantile3 = dataframe_1.quantile(0.25)
Quantile4 = dataframe_1.quantile(0.75)
Quantile_Difference = Quantile4 - Quantile3
dfout_1 = dataframe_1[~((dataframe_1 < (Quantile3 - 1.5 * Quantile_Difference)) |(dataframe_1 > (Quantile4 + 1.5 * Quantile_Difference))).any(axis=1)]
dfout_1.shape

DECISION = []
for i in dfout_1['ACTIVITY']:
    if i == 3:
        DECISION.append('1')
    else: 
        DECISION.append('0')
dfout_1['DECISION'] = DECISION
print(dfout_1.head(10))

X_split1 = dfout_1[['TIME','SL','EEG','BP']]
Y_split1 = dfout_1['DECISION']
print(X_split1.shape)
print(Y_split1.shape)

X_train1, X_test1, y_train1, y_test1 = train_test_split(X_split1, Y_split1, test_size=0.1, random_state=50)
sc1 = StandardScaler()
#sc = MinMaxScaler()
X_train1 = sc1.fit_transform(X_train1)
X_test1 = sc1.fit_transform(X_test1)

print(X_train1.shape)
print(y_train1.shape)
print(X_test1.shape)
print(y_test1.shape)

"""Perform Random Forest Classifier with Feature Importance and Forward Feature Selection.



"""

rf = RandomForestClassifier()
rf.fit(X_train1,y_train1)
rf_predict = rf.predict(X_test1)

# Print confusion matrix and accuracy score
rf_conf_matrix = confusion_matrix(y_test1, rf_predict)
rf_acc_score = accuracy_score(y_test1, rf_predict)
rf_class_report = classification_report(y_test1, rf_predict)
print(rf_conf_matrix)
print('Accuracy Score :','%.2f' %rf_acc_score)
print('Classification Report :')
print(rf_class_report)

skf = StratifiedKFold(n_splits=10, random_state=None)
skf.get_n_splits(X_split1,Y_split1)

accuracy=[]

for train_index, test_index in skf.split(X_split1, Y_split1):
    #print('Train :' , train_index, 'Test : ', test_index)
    X1_train1, X1_test1 = X_split1.iloc[train_index], X_split1.iloc[test_index]
    y1_train1, y1_test1 = Y_split1.iloc[train_index], Y_split1.iloc[test_index]
    
    rf.fit(X1_train1, y1_train1)
    prediction = rf.predict(X1_test1)
    score = accuracy_score(prediction, y1_test1)
    accuracy.append(score)
    
print(accuracy)
print('Mean accuracy :')
print('%.2f' %np.array(accuracy).mean())

