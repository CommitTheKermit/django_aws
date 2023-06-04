from django.shortcuts import render
import json
from django.http import JsonResponse  

from .models import Cafe
from . import recommend

# Create your views here.

def recommend_cafes_base_keyword(request):
	data = json.loads(request.body.decode('utf-8'))
	user_cafe_profile = data['user_cafe_profile']
	user_location = data['user_location']

	recommend_cafe = recommend.recommend_cafe_base_keyworkd(user_cafe_profile, user_location)	
	#recommend_cafe = Cafe.objects.filter(cafe_id__in=recommend_cafe_id_list)
	json_data = recommend_cafe.to_json(orient='records')

	return JsonResponse(json_data, safe=False, status=200)


def recommend_cafes_base_rating(request):
	data = json.loads(request.body.decode('utf-8'))
	user_location = data['user_location']


	recommend_cafe = recommend.recommend_cafe_base_rating(user_location)
	json_data = recommend_cafe.to_json(orient='records')

	return JsonResponse(json_data, safe=False, status=200)


# def get_reviewed_cafes(request):
