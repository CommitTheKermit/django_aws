from rest_framework import serializers
from .models import User, CafeInfo

class User_basic_serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_email', 'user_name', 'user_type', 'user_nickname',\
                  'user_age', 'user_sex')

class Cafe_info_serializer(serializers.ModelSerializer):
    class Meta:
        model = CafeInfo
        fields = ('cafe_id','cafe_add_name', 'cafe_name', 'cafe_rating', 'visitor_reviews', 'blog_reviews',\
                  'address',  'latitude', 'longitude','cafe_buisiness_hour', 'cafe_phone', 'cafe_link',\
                    'cafe_desc')