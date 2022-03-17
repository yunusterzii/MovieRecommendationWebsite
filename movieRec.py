import pandas as pd
import numpy as np
import json
from flask import Flask,request,render_template, redirect, url_for

from tmdbv3api import TMDb
from tmdbv3api import Movie

rates = {}
movie_list = []
predict_users = {}
random_user = pd.DataFrame()

app = Flask(__name__)

@app.route("/")
def index():
    G = 31
    return render_template('index.html', G = G)

@app.route("/movierates",methods=['GET', 'POST'])
def getRates():
    if request.method == "POST":

        ulWithRateInfo = request.form.get("ratedName")
        ulToDict = json.loads(ulWithRateInfo)

        for x in range(len(ulToDict)):
            rateValue = ulToDict[x]['value'][1]
            if rateValue == None:
                rateValue = 0
            rateValue = rateValue / 2   
            rates[int(ulToDict[x]['value'][0])] = float(rateValue)

        createUser()
        createPredictedUsers()
        createMovieList()


        return redirect(url_for("movielist"))
    else:
        return render_template("index.html")  
    

movies = pd.read_csv("movies1.csv", index_col = False)
ratings = pd.read_csv("ratings1.csv", index_col = False)

################################################################

tmdb = TMDb()
tmdb.api_key = '8151741cef380652f287f81ee920821d'
tmdb.language = 'en'
tmdb.debug = True

################################################################


movies.drop("genres",axis=1,inplace = True)
ratings.drop("timestamp",axis=1,inplace = True)

for i in range(1,len(ratings["userId"].unique())+1):
    a = ratings[ratings.userId == i]
    if len(a) < 100:
        ratings = ratings[ratings.userId != i]

rating_matrix = ratings.pivot_table(index = 'userId', columns = 'movieId', values = 'rating')

rating_matrix_bias_fill = rating_matrix.fillna(0)

def fill(row):
    new_row = ((row - row.mean())/(row.max() - row.min()))
    return new_row

rating_matrix_bias_fill = rating_matrix_bias_fill.apply(fill)

from sklearn.metrics.pairwise import cosine_similarity


def createUser():
    random = pd.DataFrame(columns=rating_matrix.columns)
    random.loc[1,:] = 0
    for i in rates.keys():
        random[i] = rates[i]

    random_array = np.array(random[random.index == 1])
    new_random = (random_array - random_array.mean())/(random_array.max() - random_array.min())
    global random_user
    random_user = pd.DataFrame(new_random)

    return random_user


def createPredictedUsers():
    test_ratings = rating_matrix_bias_fill
    userIds = test_ratings.index.tolist()
    sim = cosine_similarity(random_user,test_ratings)[0].tolist()
    values = dict(zip(userIds,sim))
    sorted_values = {}
    for i in sorted(values.values(),reverse = True):
        key = None
        for j in values.keys():
            if values[j] == i:
                key = j
        sorted_values[key] = i

    global predict_users
    for i in sorted_values.keys():
        if sorted_values[i] != 0:
            predict_users[i] = sorted_values[i]
        if len(predict_users) == 5:
            break
    
    return predict_users


def point(movieId):
    a = []
    for i in predict_users.keys():
        rate = rating_matrix_bias_fill[rating_matrix_bias_fill.index == i][movieId]
        a.append(float(rate) * predict_users[i])
    point = sum(a)/sum(predict_users.values())
    return point


def createMovieList():
    movie_recs = {}
    a = {}
    for i in rating_matrix_bias_fill.columns:
        a[i] = point(i)

    a_sorted = dict(sorted(a.items(), key=lambda x : x[1], reverse = True))
    for i in a_sorted.keys():
        if i in rates.keys():
            continue
        movie_recs[i] = a_sorted[i]
        if len(movie_recs) == 10:
            break

    for i in movie_recs.keys():
        movie = movies[movies.movieId == i]["title"].tolist()
        movie_list.append(movie)
    return movie_list

def remove_non_ascii_1(text):
    return ''.join([i if ord(i) < 128 else ' ' for i in text])   


@app.route("/movielist")
def movielist():
    text = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="/static/style.css">
        <title>Movie App</title>
    </head>
    <body>
    
        <header>
            <div class="container-logo">
                <img src="https://img.icons8.com/ios/50/000000/home--v1.png" alt="Homepage" onClick="goHome()"/>
            </div>            

            <div class="container-search">
            <form id="form">
                <input type="text" placeholder="Search" id="search" class="search">
            </form>
            </div>
        </header>
        <main id="main">
            <h1 class="rec-title">Recommended for you:</h1>
            <div class="padding-div">
    '''

    for i in range(len(movie_list)):
        thisMovie_name = (str(movie_list[i]))[2:len(str(movie_list[i]))-8]
        thisMovie_year = (str(movie_list[i]))[len(str(movie_list[i]))-7:len(str(movie_list[i]))-3]
        thisMovie_id = 0
        thisMovie_poster_path = ""
        thisMovie_overview = ""
        thisMovie_vote_average = 0
        vote_averageColor = ""
        thisMovie_date = ""

        substring_the = ", The"
        substring_a = ", A"
        substring_an = ", An"

        if substring_the in thisMovie_name:
            thisMovie_name = "The " + thisMovie_name[:len(thisMovie_name)-6]
        elif substring_a in thisMovie_name:
            thisMovie_name = "A " + thisMovie_name[:len(thisMovie_name)-4]
        elif substring_an in thisMovie_name:
            thisMovie_name = "An " + thisMovie_name[:len(thisMovie_name)-5]

        movie = Movie()
        search = movie.search(thisMovie_name)
        for s in search:
            thisMovie_date = s.release_date
            if thisMovie_year == thisMovie_date[:4]: 
                thisMovie_id = s.id
                thisMovie_overview = s.overview
                thisMovie_poster_path = s.poster_path
                thisMovie_vote_average = s.vote_average
                if thisMovie_vote_average >= 8:
                    vote_averageColor = "green"
                elif thisMovie_vote_average >= 5:
                    vote_averageColor = "orange"
                elif thisMovie_vote_average >= 0:
                    vote_averageColor = "red"           
                break

        text = text + '''
                        <div class="movie">
                            <img src="https://image.tmdb.org/t/p/w500''' + str(thisMovie_poster_path) + '''" alt="''' + str(thisMovie_name) + '''">
                            <div class="movie-info">
                                <h3>''' + str(thisMovie_name) + '''</h3>
                                <span class="''' + str(vote_averageColor) + '''">''' + str(thisMovie_vote_average) +'''</span>
                            </div>
                            <div class="overview">
                                <p>''' + str(thisMovie_overview) + '''</p>
                                <br/> 
                                <button class="know-more" id="''' + str(thisMovie_id) + '''" onClick="location.href = 'https://www.themoviedb.org/movie/''' + str(thisMovie_id) + '''';">Know More</button>
                            </div>
                        </div>
                    '''
    text = text + '''</main>
                    </div>
                    <script src="/static/script.js"></script>
                    </body>
                    </html>'''                

    text = remove_non_ascii_1(text)
    text = text.replace("�", " ")

    file = open("./templates/sum.html","w")
    file.write(text)
    file.close()
    
    movie_list.clear()
    return render_template("sum.html")

if __name__ == "__main__":
    app.run(debug = True)
