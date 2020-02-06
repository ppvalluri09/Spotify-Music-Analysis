import pandas as pd
import os
import requests
import csv
import numpy as np

def fetch_data():
	names = []
	with open('data/names.csv') as file:
		r = csv.reader(file, delimiter=",")
		for row in r:
			names.append(row[1].lower())
	names = names[1:]
	API_ENDPOINT = 'https://api.spotify.com/v1/search?q={}&type=track'
	headers = {'Accept': 'application/json', 'Content-Type': 'application/json',
			   'Authorization': 'Bearer BQAW-q08I1aXkxZRQw08YSm2BYWseQz7NIrGhLkQW_78M7Oh5Pd1tVDswPlURa3Dd02ibGP2MpK-3Rqi8jqnR6AFdLqDqfs7oJTswPBB00nlukNpQzVn36y-nw6J2i_VHjLk0jbD-KIKDc5-qhfEdoNsWMeyoiCPOlyB9MOj1y1w6iIlEUdmD_Ev30GxK4q_x0d5J5xmMciZzmkxNmuP1xVRdPLQrmXZlDOk4c7ebQ'
	}
	if not os.path.isfile('data/spotify_data_big.csv'):
		info = []
		for name in names:
			data = requests.get(API_ENDPOINT.format(name), headers=headers).json()
			for i in range(len(data['tracks']['items'])):
				info.append([data['tracks']['items'][i]['id'], data['tracks']['items'][i]['name'], data['tracks']['items'][i]['album']['artists'][0]['name']])
		

		final_df = pd.DataFrame(info, columns = ['id', 'name', 'artist_name'])
		final_df.to_csv('data/spotify_data_big.csv')

	if not os.path.isfile('data/song_data_huge.csv'):
		ids = pd.read_csv('data/spotify_data_big.csv', encoding='latin-1').iloc[:, 1].values.tolist()
		API_ENDPOINT2 = 'https://api.spotify.com/v1/audio-features/{}'
		df = pd.DataFrame(columns=['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo'])
		for ele in ids:
			data = requests.get(API_ENDPOINT2.format(ele), headers=headers).json()
			df = df.append({k: v for (k, v) in zip(data.keys(), data.values()) if k in df.columns}, ignore_index=True)
		df['name'] = pd.read_csv('data/spotify_data_big.csv', encoding='latin-1')['name'].values.tolist()
		df['artist_name'] = pd.read_csv('data/spotify_data_big.csv', encoding='latin-1')['artist'].values.tolist()
		print(df.head())
			


if os.path.isfile('data/names'):
	fetch_data()
else:
	data1 = pd.read_csv('data/top50.csv', encoding='utf-8')['Track.Name']
	data2 = pd.read_csv('data/top2018.csv', encoding='utf-8')['name']
	data3 = pd.read_csv('data/featuresdf.csv', encoding='utf-8')['name']

	df_names = pd.DataFrame()
	df_names['Names'] = list(map(lambda x: x.split('(')[0], pd.concat([data1, data2, data3], ignore_index=True)))
	df_names.to_csv('data/names.csv')

	fetch_data()