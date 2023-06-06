from django.apps import AppConfig
import pandas as pd
import pickle


class RecommendCafeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cafe'

    def ready(self):
        super().ready()

        # Load CSV file into memory here
        
        self.cafe_df = pd.read_csv("/home/ubuntu/django_aws/oasis_venv/project_oasis/cafe/cafe_df.csv", encoding="utf-8")
        self.cafe_value = pd.read_csv("/home/ubuntu/django_aws/oasis_venv/project_oasis/cafe/cafe_value.csv", encoding="utf-8")
        self.cafe_without_value = pd.read_csv("/home/ubuntu/django_aws/oasis_venv/project_oasis/cafe/cafe_without_keywords.csv", encoding="utf-8")
        self.cafe_value_x = self.cafe_value.drop(columns=['cafe_id'])

    
        with open('/home/ubuntu/django_aws/oasis_venv/project_oasis/cafe/model.pkl', 'rb') as f:
            self.rfc_model = pickle.load(f)



        # # If you want to make it globally accessible, you can do the following:
        # global cafe_df, cafe_value, cafe_without_value
        # cafe_df = self.cafe_df
        # cafe_value = self.cafe_value
        # cafe_without_value = self.cafe_without_value