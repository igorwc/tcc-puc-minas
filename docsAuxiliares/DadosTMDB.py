#!/usr/bin/env python
# coding: utf-8

import os
import json
import requests
import pandas as pd
import os.path
import time
import numpy as np

api_token = os.getenv('TMDB_KEY')
api_url_base = 'https://api.themoviedb.org/3/'

def getMovie(tmdbId):
    headers = {'Content-Type': 'application/json' }
    api_url =  '{0}movie/{1}?api_key={2}&language=en-US'.format(api_url_base,tmdbId,api_token)
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None
movies = pd.read_csv('../../../dados/movielens/ml-25m/movies.csv')
links = pd.read_csv('../../../dados/movielens/ml-25m/links.csv')
# Aqui tive que fazer um slice dos dados para não bloquear acesso à API do TMDB
temp = links[55000:]
i = 0
for index, row in temp.iterrows():
    i = i +1
    if(i%100 == 0):
        print('filmes: '+str(i))
        time.sleep(10)
    try:
        movieId = str(int(row['tmdbId']))

        if (not os.path.exists('../../../dados/tmdb/'+movieId+'.json')):
            x = getMovie(movieId)

            with open('../../../dados/tmdb/'+movieId+'.json', 'w') as outfile:
                json.dump(x, outfile, indent=4)
    except:
        continue
links.dropna(inplace=True)

links.dropna(inplace=True)
dados = []
for index, row in links.iterrows():
    movieId = str(int(row['tmdbId']))
    if (os.path.isfile('../../../dados/tmdb/'+movieId+'.json')):

        with open('../../../dados/tmdb/'+movieId+'.json') as json_file:
            print(movieId)
            data = json.load(json_file)
            if(data  is None or type( data) == None or (not 'overview' in data)):
                dados.append((row['movieId'], ''))
            else:
                dados.append((row['movieId'], data['overview']))


dados = dict(dados)
overview_df = pd.DataFrame.from_dict(dados, orient='index')
overview_df.to_csv('../../../dados/tmdb/overview.csv')
overview_df.reset_index()
overview_df['index1'] = overview_df.index
overview_df.columns = ['overview','movieId']
filmes_com_overview = pd.merge(movies, overview_df, on="movieId", how="right")

filmes_com_overview['overview'].replace('', np.nan, inplace=True)
filmes_com_overview.dropna(subset=['overview'], inplace=True)
filmes_com_overview.to_csv('../../../dados/movielens/filmes_com_overview.csv')
