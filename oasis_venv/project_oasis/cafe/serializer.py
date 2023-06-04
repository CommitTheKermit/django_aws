from rest_framework import serializers
from .models import Cafe

class Cafe_serializer(serializers.ModelSerializer):
    class Meta:
        model = Cafe
        fields = ('cafe_id','business_name', 'cafe_name', 'cafe_rating', 'visitor_reviews', 'blog_reviews',\
                  'cafe_phone_number', 'cafe_info', 'address',  'latitude', 'longitude')