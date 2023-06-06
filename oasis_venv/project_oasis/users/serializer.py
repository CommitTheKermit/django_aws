from rest_framework import serializers
from .models import Customer

class Customer_basic_serializer(serializers.ModelSerializer):
    class Meta: 
        model = Customer
        fields = ('email', 'name', 'user_type', 'nickname',\
                  'age', 'sex')

# class Cafe_info_serializer(serializers.ModelSerializer):
#     class Meta:
#         model = CafeInfo
#         fields = ('cafe_id','cafe_name', 'cafe_rating', 'visitor_reviews', 'blog_reviews',\
#                   'address',  'latitude', 'longitude','cafe_buisiness_hour', 'cafe_phone', 'cafe_link',\
#                     'cafe_desc')