from django.contrib import admin
from  .models import Restaurant, RestaurantPhoto, Dish
from django.contrib import admin

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('title', 'spotlight')
    list_editable = ('spotlight',)

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(RestaurantPhoto)

admin.site.register(Dish)