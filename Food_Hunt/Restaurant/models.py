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
    

class Menu(models.Model):
    menuid = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menus')
    dishName = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    MEAL_TYPE_CHOICES = [
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
    ]
    meal_type = models.CharField(max_length=10, choices=MEAL_TYPE_CHOICES)
    time_limit = models.DurationField()
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to='menu_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.dishName} ({self.meal_type})"
    

class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')
    item_name = models.CharField(max_length=100)

    def __str__(self):
        return self.item_name
    

from django.db import models
from users.models import Users
from .models import Restaurant, Menu  # adjust if Menu is in a different app

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='orders')
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders')
    menu_id = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='orders')

    def __str__(self):
        return f"Order #{self.order_id} by {self.user.user_name}"