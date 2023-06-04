from django.shortcuts import render
import json
from django.http import JsonResponse  

from .models import Cafe
from . import distance
#코사인 유사도로 계산

# Create your views here.

def recommend_cafe(request):
	data = json.loads(request.body)
	user_cafe_profile = data.get('user_cafe_profile')
	user_location = data.get('user_location')

	recommend_cafe_id_list = distance.recommend_cafe(user_cafe_profile, user_location)
	
	recommend_cafe = Cafe.objects.filter(cafe_id__in=recommend_cafe_id_list)
	json_data = recommend_cafe.to_json(orient='records')
	return JsonResponse({'recommend_cafe_list', json_data}, status=200)
