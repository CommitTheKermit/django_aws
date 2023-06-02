from django.db import models

# # Create your models here.

# class User(models.Model):
#     user_id = models.AutoField(primary_key=True)
#     user_email = models.EmailField(max_length=255, default='none')
#     user_pw = models.CharField(max_length=60, default='none')
#     user_name = models.CharField(max_length=255, default='none')
#     user_phone = models.CharField(max_length=20, default='none')
#     user_registration_date = models.DateField(auto_now=True)
#     user_type = models.SmallIntegerField(null=True)
#     user_sex = models.SmallIntegerField(null=True)
#     user_age = models.SmallIntegerField(null=True)
#     user_nickname = models.CharField(max_length=20, default='none')
    
#     def __str__(self):
#         return f'{self.user_id}, {self.user_email}'
    
#     class Meta:
#         db_table = 'users_Oasis'

# class EmailCode(models.Model):
#     user_email = models.EmailField(max_length=255, default='none')
#     user_code = models.CharField(max_length=6)

#     class Meta:
#         db_table = 'email_code_Oasis'



class User(models.Model):
    USER_TYPE_CHOICES = [
        ('Customer', 'Customer'),
        ('Employee', 'Employee'),
    ]
    
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, default='none')
    password = models.CharField(max_length=60, default='none')
    name = models.CharField(max_length=255, default='none')
    phone_no = models.CharField(max_length=20, default='none')
    registration_date = models.DateTimeField(auto_now_add=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    
    class Meta:
        db_table = 'User'

class Customer(User):
    SEX_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    nickname = models.CharField(max_length=15)
    age = models.IntegerField()
    sex = models.CharField(max_length=6, choices=SEX_CHOICES)

    def __str__(self):
        return f'{self.user_id}, {self.user_email}'
    
    class Meta:
        db_table = 'Customer'


class EmailCode(models.Model):
    user_email = models.EmailField(max_length=255, default='none')
    user_code = models.CharField(max_length=6)

    class Meta:
        db_table = 'EmailCode'