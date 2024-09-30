from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class Restaurant(models.Model):

    DIETARY_CHOICES = [
        ('veg' , 'Vegetarian'),
        ('vegan', 'Vegan'),
        ('non-veg', 'Non vegetarian'),
        
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    cost_for_two = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    location = models.CharField(max_length=255)
    address= models.TextField()
    timings = models.CharField(max_length=20)
    dietary_preference = models.CharField(max_length=20, choices=DIETARY_CHOICES)
    spotlight = models.BooleanField(default=False)


    def __str__(self):
        return self.title
    
    def update_rating(self):
        avg_rating = self.reviews.aggregate(Avg('rating'))['rating__avg']

        if avg_rating is not None:
            self.rating = round(avg_rating, 1)
        else:
            self.rating=0.0
        self.save()

        
class RestaurantPhoto(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='photos', on_delete=models.CASCADE)
    image=models.ImageField(upload_to = 'restaurant_photos/')
    uploaded_at = models.DateTimeField(auto_now_add = True)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'Photo of {self.restaurant.title}'
    
class Dish(models.Model):

    CUISINE_CHOICES = [
        ('NI', 'North Indian'),
        ('SI', 'South Indian'),
        ('EI', 'East Indian'),
        ('IF', 'Indian Fusion'),
    ]

    name = models.CharField(max_length=255)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    is_veg = models.BooleanField(default=False)
    image = models.ImageField(upload_to='dish_photos/', null=True, blank=True)
    is_deleted= models.BooleanField(default=False)
    cuisine_type = models.CharField(max_length=20, choices=CUISINE_CHOICES)

    def __str__(self):
        return f'{self.name} of {self.restaurant.title}'
    

class Review(models.Model):

    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, related_name='reviews', on_delete=models.CASCADE)
    rating = models.FloatField(
        validators=[
            MinValueValidator(1.0),
            MaxValueValidator(5.0)
        ],
        help_text="Rating must be between 1.0 and 5.0."
    )
    # rating = models.DecimalField(max_digits=2, decimal_places=1)
    comment = models.TextField()

    def __str__(self):
        return f'{self.user.username} gave {self.rating} to {self.restaurant}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.restaurant.update_rating()


class VisitedRestaurant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, related_name='visits', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.restaurant.title}'
    

class BookmarkedRestaurant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, related_name='bookmarks' ,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.restaurant.title}'
