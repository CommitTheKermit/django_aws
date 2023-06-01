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
    cafe = models.OneToOneField(Cafe, on_delete=models.CASCADE, primary_key=True)
    dessert = models.DecimalField(max_digits=12, decimal_places=10)
    well_being = models.DecimalField(max_digits=12, decimal_places=10)
    various_menu = models.DecimalField(max_digits=12, decimal_places=10)
    special_menu = models.DecimalField(max_digits=12, decimal_places=10)
    pleasant_store = models.DecimalField(max_digits=12, decimal_places=10)
    clean_store = models.DecimalField(max_digits=12, decimal_places=10)
    background = models.DecimalField(max_digits=12, decimal_places=10)
    parking = models.DecimalField(max_digits=12, decimal_places=10)
    comfort = models.DecimalField(max_digits=12, decimal_places=10)
    calm_down = models.DecimalField(max_digits=12, decimal_places=10)
    trendy_store = models.DecimalField(max_digits=12, decimal_places=10)
    unique_store = models.DecimalField(max_digits=12, decimal_places=10)
    price = models.DecimalField(max_digits=12, decimal_places=10)
    gift_packaging = models.DecimalField(max_digits=12, decimal_places=10)
    alcohol = models.DecimalField(max_digits=12, decimal_places=10)
    baby = models.DecimalField(max_digits=12, decimal_places=10)
    service = models.DecimalField(max_digits=12, decimal_places=10)
    activity = models.DecimalField(max_digits=12, decimal_places=10)
    label = models.IntegerField()

    class Meta:
         db_table = 'CafeKeywords'