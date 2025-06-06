from django.db import models
from django.contrib.auth.hashers import make_password, check_password


# Create your models here.
USER_TYPES = (
        ('admin', 'admin'),
        ('user', 'user'),
        ('restaurant', 'restaurant'),
    )

class Users(models.Model):
    user_id = models.AutoField(primary_key=True,)
    user_name = models.CharField(max_length=100)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    email_ID = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def _str_(self):
        return self.username
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)