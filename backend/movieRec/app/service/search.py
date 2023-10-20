import pandas as pd
import requests
import json


def search(query):
    tmdbIDs = getTmdbIDs()
    searchIds = getSearchIds(query)
    return list(set(tmdbIDs).intersection(set(searchIds)))


def getTmdbIDs():
    links = pd.read_csv("app\\data\\links.csv", index_col=False)
    tmdbIDs = set(links["tmdbId"].to_list())

    return tmdbIDs


def getSearchIds(query):
    api_key = "8151741cef380652f287f81ee920821d"
    url = "https://api.themoviedb.org/3/search/movie?api_key=" + \
        api_key + "&page=1&language=" + "&query=" + query
    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)
    data_raw = response.text
    data = json.loads(data_raw)

    return set([movie["id"] for movie in data["results"]])
