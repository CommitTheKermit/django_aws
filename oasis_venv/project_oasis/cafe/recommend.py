from haversine import haversine, Unit
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.ensemble import RandomForestClassifier

from django.apps import apps
import pandas as pd

app_config = apps.get_app_config('cafe')

cafe_df = app_config.cafe_df
cafe_value = app_config.cafe_value
cafe_without_value = app_config.cafe_without_value
cafe_value_x = app_config.cafe_value_x

rfc_model = app_config.rfc_model

# 두 위치 간 거리를 구하는 함수
def calculate_distance(user_location, cafe_location):
    distance = haversine(user_location, cafe_location, unit=Unit.KILOMETERS)
    return distance

#현재 사용자 위치 기준 3km 이내 카페의 id list 반환 함수
def get_cafe_list_base_location(user_location, max_distance=3.0):
    nearby_cafes = []
    for idx, row in cafe_df.iterrows():
        cafe_location = (row['위도'], row['경도'])
        distance = calculate_distance(user_location, cafe_location)
        if distance <= max_distance:
            nearby_cafes.append(row['cafe_id'])

    return nearby_cafes

def create_user_cafe_profile_df(user_cafe_profile):
    cafe_value_columns_list = ['beverage', 'dessert', 'various_menu', 'special_menu', 'large_store', 'background', 'talking', 'concentration', 'trendy_store']
    return pd.DataFrame([user_cafe_profile], columns=cafe_value_columns_list )

def classify_with_random_forest(neary_cafes_value, user_cafe_profile):
    # 랜덤 포레스트 모델로 카페 데이터 학습 -> grid search 로 찾은 최적의 파라미터 사용
    return  rfc_model.predict(create_user_cafe_profile_df(user_cafe_profile))

def calculate_cosine_similarity(neary_cafes_value, user_cafe_profile):
    return cosine_similarity(neary_cafes_value, create_user_cafe_profile_df(user_cafe_profile))


def recommend_cafe_base_keyworkd(user_cafe_profile, user_location, range=3):
    #근처 카페 id list로 데이터 프레임 불러오기
    neary_cafes_list = get_cafe_list_base_location(user_location, range)
    neary_cafes_value_df = cafe_value[cafe_value['cafe_id'].isin(neary_cafes_list)]

    #랜덤 포레스트로 분류 과정에 불필요한 열 값들은 제거
    neary_cafes_value_df = neary_cafes_value_df.drop(columns=['cafe_id', 'low_price', 'high_price', 'parking', 'gift_packaging', 'common_keywords'])

    #랜덤 포레스트 모델로 라벨 값 분류해서 라벨에 해당하는 근처 카페 추출
    classified_label = classify_with_random_forest(neary_cafes_value_df, user_cafe_profile)
    neary_cafes_value_df = neary_cafes_value_df[neary_cafes_value_df['label'] == classified_label[0]]

    #코사인 유사도 계산 과정에 불필요한 열 값들은 제거
    neary_cafes_value_df = neary_cafes_value_df.drop(columns=['label'])

    #사용자 선호 카페 프로필 값으로 코사인 유사도 계산
    similarities = calculate_cosine_similarity(neary_cafes_value_df, user_cafe_profile)
    neary_cafes_value_df['similarity'] = similarities

	#코사인 유사도가 가장 높은 2개의 카페를 리스트에 저장
    top_two_cafe_df = neary_cafes_value_df['similarity'].nlargest(2).index.to_list()
    recommend_cafe_list = cafe_value.loc[top_two_cafe_df, 'cafe_id'].to_list()

	#키워드와 별점이 존재하지 않는 카페 리스트에서 랜덤으로 카페 하나를 추출해 리스트에 저장
    neary_cafes_value_df = cafe_without_value.sample(1)
    recommend_cafe_list.append(neary_cafes_value_df['cafe_id'].values[0])

    recommend_cafe = cafe_df.iloc[recommend_cafe_list]
	
    return recommend_cafe


def recommend_cafe_base_rating(user_location):
    #근처 카페 id list로 데이터 프레임 불러오기 + 별점도 불러오기
    neary_cafes_list = get_cafe_list_base_location(user_location)
    neary_cafes_value_df = cafe_value[cafe_value['cafe_id'].isin(neary_cafes_list)]
    neary_cafes_value_df['rating'] = cafe_df.loc[neary_cafes_value_df['cafe_id'], '별점'].to_list()

    # 공통 키워드 값과 별점 값의 총합이 가장 높은 top 3 추천
    neary_cafes_value_df = neary_cafes_value_df[['common_keywords', 'rating']]
    top_three_cafe_df = neary_cafes_value_df.sum(axis=1).nlargest(3)
    
    recommend_cafe = cafe_df.loc[cafe_value.loc[top_three_cafe_df.index, 'cafe_id']]
    
    return recommend_cafe






    

    

    

