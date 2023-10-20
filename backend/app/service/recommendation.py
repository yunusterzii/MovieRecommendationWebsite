from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np


def getRecommendedMovies(user_rates):
    ratings, links = createTables()
    rates = {}
    ids = links["movieId"].tolist()
    tmdbs = links["tmdbId"].tolist()

    id_to_tmdb = dict(zip(ids, tmdbs))
    tmdb_to_id = dict(zip(tmdbs, ids))

    for rate in user_rates:
        movieId = tmdb_to_id[rate["movieID"]]
        rates[movieId] = rate["value"]

    rating_matrix = ratings.pivot_table(
        index='userId', columns='movieId', values='rating')

    rating_matrix_bias_fill = rating_matrix.fillna(0)
    rating_matrix_bias_fill = rating_matrix_bias_fill.apply(mean_normalization)

    user = createUser(rating_matrix, rates)
    predict_users = createPredictedUsers(rating_matrix_bias_fill, user)
    recommended_movies = createMovieList(rating_matrix_bias_fill,
                                         predict_users, rates, id_to_tmdb)
    return recommended_movies


def createTables():
    ratings = pd.read_csv("app\\data\\ratings.csv", index_col=False)
    links = pd.read_csv("app\\data\\links.csv", index_col=False)

    ratings.drop("timestamp", axis=1, inplace=True)
    links.drop("imdbId", axis=1, inplace=True)

    for i in range(1, len(ratings["userId"].unique())+1):
        a = ratings[ratings.userId == i]
        if len(a) < 100:
            ratings = ratings[ratings.userId != i]

    return ratings, links


def mean_normalization(row):
    new_row = ((row - row.mean())/(row.max() - row.min()))
    return new_row


def createUser(rating_matrix, rates):
    user = pd.DataFrame(columns=rating_matrix.columns)
    user.loc[1, :] = 0
    for i in rates.keys():
        user[i] = rates[i]

    user_array = np.array(user[user.index == 1])
    new_user_array = (user_array - user_array.mean()) / \
        (user_array.max() - user_array.min())
    new_user = pd.DataFrame(new_user_array)

    return new_user


def createPredictedUsers(rating_matrix_bias_fill, user):
    test_ratings = rating_matrix_bias_fill
    userIds = test_ratings.index.tolist()
    sim = cosine_similarity(user, test_ratings)[0].tolist()
    values = dict(zip(userIds, sim))
    sorted_values = {}
    for i in sorted(values.values(), reverse=True):
        key = None
        for j in values.keys():
            if values[j] == i:
                key = j
        sorted_values[key] = i

    predict_users = {}
    for i in sorted_values.keys():
        if sorted_values[i] != 0:
            predict_users[i] = sorted_values[i]
        if len(predict_users) == 5:
            break

    return predict_users


def point(movieId, predict_users, rating_matrix_bias_fill):
    a = []
    for i in predict_users.keys():
        rate = rating_matrix_bias_fill[rating_matrix_bias_fill.index == i][movieId]
        a.append(float(rate) * predict_users[i])
    point = sum(a)/sum(predict_users.values())
    return point


def createMovieList(rating_matrix_bias_fill, predict_users, rates, id_to_tmdb):
    movie_list = []
    a = {}
    for i in rating_matrix_bias_fill.columns:
        a[i] = point(i, predict_users, rating_matrix_bias_fill)

    a_sorted = dict(sorted(a.items(), key=lambda x: x[1], reverse=True))
    for i in a_sorted.keys():
        if i in rates.keys():
            continue
        movie_list.append(id_to_tmdb[i])
        if len(movie_list) == 15:
            break

    return movie_list
