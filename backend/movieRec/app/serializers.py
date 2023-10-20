from rest_framework import serializers
from .models import Rate
from .models import Movie

class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ['id', 'movieID', 'value']
    
    class Meta:
        model = Movie
        fields = ['id', 'movieID']