from django.apps import AppConfig
import pandas as pd
import numpy as np



class RecommendCafeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cafe'

    def ready(self):
        super().ready()

        # Load CSV file into memory here
        
        self.cafe_df = pd.read_csv("./좌표 처리전_이상치 삭제.csv", encoding="utf-8")
        self.cafe_value = pd.read_csv("./k-means 클러스터링 처리4.csv", encoding="utf-8")
        self.cafe_without_value = pd.read_csv("./cafe_without_keywords.csv", encoding="utf-8")
        self.cafe_value_x = self.cafe_value.drop(columns=['cafe_id'])

        # # If you want to make it globally accessible, you can do the following:
        # global cafe_df, cafe_value, cafe_without_value
        # cafe_df = self.cafe_df
        # cafe_value = self.cafe_value
        # cafe_without_value = self.cafe_without_value