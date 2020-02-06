import pandas as pd
import os
import requests

def fetch_data():
	names = pd.read_csv('data/names.csv').iloc[:, 1].values.tolist()
	API_ENDPOINT = 'https://api.spotify.com/v1/search?q={}&type=track'
	headers = {'Accept': 'application/json', 'Content-Type': 'application/json',
			   'Authorization': 'Bearer BQBnz_5kNwqVx-GRqf0dEsaMtqWWg69Z0vtuKBxLBkklz1LoB4XPVFHmOmVc2KREP96emj2jahFrZnM77mIvx2cm47hlV2eXbYLusoauWllWI7RVWnKUQoOKrNehrW3fhNsSfdVdtRoqt22UxYN3F4YrzFIL8tViyRtqnpTTAQwKottAWEfLxTdg1bS2_nNCm7zrDBZKkCMi7QZhLhL0hNTlG7IUqPyh_5jWrvR6pQ'
	}
	ids = []
	for name in names:
		data = requests.get(API_ENDPOINT.format(name), headers=headers).json()
		print(data['tracks'])
		break


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