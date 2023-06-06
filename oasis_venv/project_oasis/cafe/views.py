import json
from django.http import JsonResponse  

from . import recommend

# Create your views here.

# 사용자의 선호 프로필를 이용해 유사한 키워드를 가진 카페 추천
def recommend_cafes_base_keyword(request):
	data = json.loads(request.body.decode('utf-8'))
	user_cafe_profile = data['user_cafe_profile']
	user_location = data['user_location']

	recommend_cafe = recommend.recommend_cafe_base_keyworkd(user_cafe_profile, user_location)	
	#recommend_cafe = Cafe.objects.filter(cafe_id__in=recommend_cafe_id_list)
	json_data = recommend_cafe.to_json(force_ascii=False, orient='records')
	data = json.loads(json_data)
	return JsonResponse(data, safe=False, status=200)
	


# 평점과 자체 공통 키워드를 이용해 TOP 3 카페를 추천
def recommend_cafes_base_rating(request):
	data = json.loads(request.body.decode('utf-8'))
	user_location = data['user_location']


	recommend_cafe = recommend.recommend_cafe_base_rating(user_location)
	json_data = recommend_cafe.to_json(force_ascii=False, orient='records')
	data = json.loads(json_data)
	
	return JsonResponse(data, safe=False, status=200)
	# return JsonResponse(json.dump(json_data), safe=False, status=200)


# def get_reviewed_cafes(request):
