from django.contrib import admin
from  .models import Restaurant, RestaurantPhoto, Dish

# Register your models here.
admin.site.register(Restaurant)
admin.site.register(RestaurantPhoto)

admin.site.register(Dish)