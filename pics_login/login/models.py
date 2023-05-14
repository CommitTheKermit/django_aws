from django.db import models

# Create your models here.

class User(models.Model):
    user_id = models.CharField(max_length=20)
    user_pw = models.CharField(max_length=20)
    user_phone  = models.CharField(max_length=20)
    
    def __str__(self):
        return f'{self.user_id}, {self.user_pw}, {self.user_phone}'
    
    class Meta:
        db_table = 'users_custom'