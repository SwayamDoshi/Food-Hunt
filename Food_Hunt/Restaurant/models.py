from django.db import models
from users.models import Users

class Restaurant(models.Model):
    CATEGORY_CHOICES = (
        ('preorder', 'Preorder Kitchen'),
        ('normal', 'Instant Restaurant'),
    )
    res_id = models.AutoField(primary_key=True,)
    user_id = models.ForeignKey(Users,on_delete=models.CASCADE,limit_choices_to={'user_type':'restaurant'})
    res_number = models.CharField(max_length=15)
    res_name = models.CharField(max_length=100)
    res_address = models.TextField()
    fssai_no = models.CharField(max_length=50)
    res_picture = models.ImageField(upload_to='restaurant_pics/')
    res_cat = models.CharField(max_length=10, choices=CATEGORY_CHOICES)

    def _str_(self):
        return self.res_name
# Create your models here.
