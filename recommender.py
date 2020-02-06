import pandas as pd
import numpy as np
import seaborn as sns
import numpy as np
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler, MinMaxScaler, Normalizer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.cluster import MeanShift, KMeans, Birch
from sklearn.decomposition import PCA
import pickle


df = pd.read_csv('data/song_data_small.csv').iloc[:, 1:]

colors = ['r', 'b', 'g', 'y', 'c'] * 2
# Distribution plots for each feature
# for i in range(df.shape[1] - 2):
# 	plt.subplot(3, 3, i + 1)
# 	sns.distplot(df.iloc[:, i], color=colors[i])
# plt.show()

# Feature Scaling the data
x = df.iloc[:, :-2].copy()
# print(x.describe())
x.iloc[:] = StandardScaler().fit_transform(x)

# Normalizing the datapoints
x.iloc[:] = Normalizer().fit_transform(x)

# Distribution plot of features after feature scaling
# print(x.head())
# for i in range(x.shape[1]):
# 	plt.subplot(3, 3, i + 1)
# 	sns.distplot(x.iloc[:, i], color=colors[i])
# plt.show()

# def cluster(model, x):
# 	return model.fit(x)

cluster = lambda model, x: model.fit(x)

brc = cluster(Birch(), x)
kmeans = cluster(KMeans(n_clusters=4), x)
mft = cluster(MeanShift(), x)

# Birch seems relatively better since it clusters the datapoints into 3 clusters which it identifies
# print(brc.labels_)
# KMeans seems ambiguous to use since we cannot define the way the data can be clustered and into how many clusters 
# print(kmeans.labels_)
# MeanShift doesn't yield any useful results
# print(mft.labels_)

# Reducing the dimension to 2-D for viz purpose
x_reduced = PCA(n_components=2).fit_transform(x)
for i in range(len(brc.labels_)):
	plt.scatter(x_reduced[i][0], x_reduced[i][1], c=colors[brc.labels_[i]], edgecolors='black', alpha=0.6)
plt.show()

with open('models/model.sav', 'wb') as file:
	pickle.dump(brc, file)