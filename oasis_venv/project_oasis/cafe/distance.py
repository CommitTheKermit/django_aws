from haversine import haversine, Unit
from sklearn.metrics.pairwise import cosine_similarity
from django.apps import apps
import pandas as pd

app_config = apps.get_app_config('cafe')

cafe_df = app_config.cafe_df
cafe_value = app_config.cafe_value
cafe_without_value = app_config.cafe_without_value
cafe_value_x = app_config.cafe_value_x

# 두 위치 간 거리를 구하는 함수
def calculate_distance(user_location, cafe_location):
    distance = haversine(user_location, cafe_location, unit=Unit.KILOMETERS)
    return distance


#현재 사용자 위치 기준 3km 이내 카페의 id list 반환 함수
def get_cafe_list_location(user_location, max_distance=3.0):
    nearby_cafes = []
    for index, row in cafe_df.iterrows():
        cafe_location = (row['위도'], row['경도'])
        distance = calculate_distance(user_location, cafe_location)
        if distance <= max_distance:
            nearby_cafes.append(row['cafe_id'])
    return nearby_cafes

def recommend_cafe(user_cafe_profile, user_location, range=3):
    neary_cafes_list = get_cafe_list_location(user_location, range)
    neary_cafes_value = cafe_value_x.iloc[cafe_value[cafe_value['cafe_id'].isin(neary_cafes_list)].index]

    cafe_value_columns_list = [
	    '디저트', '다양한 메뉴', '특별한 메뉴', '쾌적한 매장',  '야외 배경', '주차', 
        '대화', '집중', '트렌디', '독특', '선물, 포장', '액티비티'
    ]
    user_value = pd.DataFrame([user_cafe_profile], columns=cafe_value_columns_list )
    similarities = cosine_similarity(neary_cafes_value, user_value)
    neary_cafes_value['similarity'] = similarities

	#코사인 유사도가 가장 높은 2개의 카페를 리스트에 저장
    top_two_cafe_value = cafe_random_list['similarity'].nlargest(2).index.to_list()
    recommend_cafe_list = cafe_value.loc[top_two_cafe_value, 'cafe_id'].to_list()

	#키워드와 별점이 존재하지 않는 카페 리스트에서 랜덤으로 카페 하나를 추출해 리스트에 저장
    cafe_random_list = cafe_without_value.sample(1)
    recommend_cafe_list.append(cafe_random_list['cafe_id'].values[0])
	
    return recommend_cafe_list

