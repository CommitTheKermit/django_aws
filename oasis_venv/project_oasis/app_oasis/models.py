from django.db import models

# Create your models here.

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_email = models.EmailField(max_length=255, default='none')
    user_pw = models.CharField(max_length=60, default='none')
    user_name = models.CharField(max_length=255, default='none')
    user_phone = models.CharField(max_length=20, default='none')
    user_registration_date = models.DateField(auto_now=True)
    user_type = models.SmallIntegerField(null=True)
    user_sex = models.SmallIntegerField(null=True)
    user_age = models.SmallIntegerField(null=True)
    user_nickanme = models.CharField(max_length=20, default='none')
    
    def __str__(self):
        return f'{self.user_id}, {self.user_email}'
    
    class Meta:
        db_table = 'users_Oasis'

class EmailCode(models.Model):
    user_email = models.EmailField(max_length=255, default='none')
    user_code = models.CharField(max_length=6)

    class Meta:
        db_table = 'email_code_Oasis'

class CafeInfo(models.Model):
    cafe_id = models.CharField(primary_key=True, unique=True, max_length=10)
    cafe_add_name = models.CharField(max_length=255)
    cafe_name = models.CharField(max_length=255)
    cafe_rating = models.CharField(max_length=10)
    visitor_reviews = models.CharField(max_length=10)
    blog_reviews = models.CharField(max_length=10)
    address = models.CharField(max_length=255)
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)
    cafe_buisiness_hour = models.TextField()
    cafe_phone = models.CharField(max_length=20)
    cafe_link = models.CharField(max_length=255)
    cafe_desc = models.TextField()

    class Meta:
        db_table = 'cafe_info_Oasis'

