# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 07:51:54 2018

@author: Mathew
"""

import requests
import urllib

import pandas as pd

URL = r'https://games.crossfit.com/competitions/api/v1/competitions/open/2018/leaderboards?{params}'
entrants = []
scores = []

PARAMS = {'division': 1,
          'region': 0,
          'scaled': 0,
          'sort': 0,
          'occupation': 0,
          'page': 1}

def process_json(json):
    iter_scores = []
    iter_entrants = []
    for row in json['leaderboardRows']:
        iter_entrants.append(row['entrant'])
        for score in row['scores']:
            score['competiorId'] = row['entrant']['competitorId']
            iter_scores.append(score)
    return iter_entrants, iter_scores


pages = True
while pages:
    data = requests.get(URL.format(params=urllib.parse.urlencode(PARAMS)))
    if data.status_code == 200:
        json = data.json()
        
        ent, sco = process_json(json)
        entrants.extend(ent)
        scores.extend(sco)
        
        pagination = json['pagination']
        if pagination['currentPage'] == pagination['totalPages']:
            pages = False
        else:
            PARAMS['page'] += 1

entrants = pd.DataFrame(entrants)
scores = pd.DataFrame(scores)

