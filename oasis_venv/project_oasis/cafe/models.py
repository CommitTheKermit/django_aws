from django.db import models

# Create your models here.
# class Cafe(models.Model):
#     cafe_id = models.CharField(primary_key=True, unique=True, max_length=10)
#     cafe_add_name = models.CharField(max_length=255)
#     cafe_name = models.CharField(max_length=255)
#     cafe_rating = models.CharField(max_length=10)
#     visitor_reviews = models.CharField(max_length=10)
#     blog_reviews = models.CharField(max_length=10)
#     address = models.CharField(max_length=255)
#     latitude = models.CharField(max_length=20)
#     longitude = models.CharField(max_length=20)
#     cafe_buisiness_hour = models.TextField()
#     cafe_phone = models.CharField(max_length=20)
#     cafe_link = models.CharField(max_length=255)
#     cafe_desc = models.TextField()

#     class Meta:
#         db_table = 'Cafe'


class Cafe(models.Model):
    cafe_id = models.AutoField(primary_key=True)
    business_name = models.CharField(max_length=255)
    cafe_name = models.CharField(max_length=255)
    cafe_rating = models.DecimalField(max_digits=3, decimal_places=2)
    visitor_review_number = models.IntegerField()
    blog_review_number = models.IntegerField()
    cafe_phone_number = models.CharField(max_length=20)
    cafe_info = models.TextField()
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    cafe_image = models.ImageField(upload_to='cafes/images/',  blank=True)

    class Meta:
         db_table = 'Cafe'

class CafeKeywords(models.Model):
    RATING_CHOICES = [
            (1, '1'),
            (2, '2'),
            (3, '3'),
            (4, '4'),
            (5, '5'),
        ]

    cafe = models.OneToOneField(Cafe, on_delete=models.CASCADE, primary_key=True)
    dessert = models.IntegerField(choices=RATING_CHOICES)
    various_menu = models.IntegerField(choices=RATING_CHOICES)
    special_menu = models.IntegerField(choices=RATING_CHOICES)
    large_store = models.IntegerField(choices=RATING_CHOICES)
    background = models.IntegerField(choices=RATING_CHOICES)
    parking = models.IntegerField(choices=RATING_CHOICES)
    talking = models.IntegerField(choices=RATING_CHOICES)
    concentration = models.IntegerField(choices=RATING_CHOICES)
    trendy_store = models.IntegerField(choices=RATING_CHOICES)
    unique_store = models.IntegerField(choices=RATING_CHOICES)
    gift_packaging = models.IntegerField(choices=RATING_CHOICES)
    
    class Meta:
         db_table = 'CafeKeywords'