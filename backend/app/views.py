from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from app.service.recommendation import getRecommendedMovies
from app.service.search import search
from app.service.movies import getRandomMovies


@api_view(['POST'])
def submitRates(request):
    data = request.data["data"]
    movies = getRecommendedMovies(data)
    return Response(movies, status=status.HTTP_200_OK)


@api_view(['POST'])
def searchQuery(request):
    print(request.data)
    query = request.data["query"]
    searchMovies = search(query)
    return Response(searchMovies, status=status.HTTP_200_OK)


@api_view(['GET'])
def getMovies(request):
    movies = getRandomMovies()
    return Response(movies, status=status.HTTP_200_OK)
