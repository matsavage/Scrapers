# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 07:51:54 2018

@author: Mathew
"""

import os
import urllib
from datetime import datetime
from json import loads as load, JSONDecodeError

import requests
import pandas as pd

URL = r'https://games.crossfit.com/competitions/api/v1/competitions/open/2018/leaderboards?{params}'
PATH = r'D:\Data\Crossfit'

PARAMS = {'division': 1,
          'region': 0,
          'scaled': 0,
          'sort': 0,
          'occupation': 0,
          'page': 1}

def process_json(data_json):
    '''Processes returned crossfit JSON into athletes and scoreboard'''
    iter_scores = []
    iter_entrants = []
    for row in data_json['leaderboardRows']:
        iter_entrants.append(row['entrant'])
        for score in row['scores']:
            score['competiorId'] = row['entrant']['competitorId']
            iter_scores.append(score)
    return iter_entrants, iter_scores


def scrape_crossfit(count=False):
    '''Scrape the crossfit games API for 2018'''
    if count:
        try:
            from mlxtend.utils import Counter
        except ImportError:
            print('Error')
            count = False
    entrants = []
    scores = []
    pages = True
    if count:
        counter = Counter(name='Scraping Crossfit Games', stderr=True)
    while pages:
        
        page = requests.get(URL.format(params=urllib.parse.urlencode(PARAMS)))
        if page.status_code == 200:
            try:
                data = page.json()
            except JSONDecodeError:
                data = load(page.text.replace('"THE ROACH"', "'THE ROACH'"))

            ent, sco = process_json(data)
            entrants.extend(ent)
            scores.extend(sco)

            pagination = data['pagination']
            end_page = pagination['currentPage'] == pagination['totalPages']
            if not end_page:
                PARAMS['page'] += 1
            elif PARAMS['division'] == 1:
                PARAMS['page'] = 1
                PARAMS['division'] += 1
            else:
                pages = False

        if count:
            counter.update()

    entrants = pd.DataFrame(entrants)
    scores = pd.DataFrame(scores)
    return entrants, scores


def main():
    '''Perform scrape and write output to file'''
    entrants, scores = scrape_crossfit(count=True)
    file = os.path.join(PATH, '{filename}-{date:%Y-%M-%D}.pickle')
    entrants.to_pickle(file.format(filename='entrants', date=datetime()))
    scores.to_pickle(file.format(filename='scores', date=datetime()))


if __name__ == '__main__':
    main()
