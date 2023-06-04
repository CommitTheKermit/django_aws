from django.shortcuts import render
from . import distance
#코사인 유사도로 계산

# Create your views here.

def recommend_cafe(request):
    neary_cafes_list = distance.get_cafe_list_location((35.8680733, 128.5995891), 3)
    neary_cafes_value = cafe_value_x.iloc[cafe_value[cafe_value['cafe_id'].isin(neary_cafes_list)].index]


	#20개의 카페 키워드 값과 사용자 프로필 값 코사인 유사도 계산
	similarities = cosine_similarity(neary_cafes_value, user_value)
    neary_cafes_value['similarity'] = similarities

	#코사인 유사도가 가장 높은 2개의 카페를 리스트에 저장
	top_two_cafe_value = cafe_random_list['similarity'].nlargest(2).index.to_list()
	recommend_cafe_list = cafe_value.loc[top_two_cafe_value, 'cafe_id'].to_list()

	#키워드와 별점이 존재하지 않는 카페 리스트에서 랜덤으로 카페 하나를 추출해 리스트에 저장
	cafe_random_list = cafe_without_value.sample(1)
	recommend_cafe_list.append(cafe_random_list['cafe_id'].values[0])
	
	return recommended_cafe_list
