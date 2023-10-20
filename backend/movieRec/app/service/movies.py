import pandas as pd
import random


def getRandomMovies():
    links = pd.read_csv("app\\data\\links.csv", index_col=False)
    tmdbIDs = links["tmdbId"].to_list()
    return random.sample(tmdbIDs, 10)
