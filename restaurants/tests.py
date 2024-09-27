from django.test import TestCase

from django.contrib.auth.models import User
from .models import Restaurant, RestaurantPhoto, Dish, Review, VisitedRestaurant, BookmarkedRestaurant
from django.core.exceptions import ValidationError
# Create your tests here.


class RestaurantModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='owner', password='password123')
        self.restaurant = Restaurant.objects.create(
            owner=self.user,
            title='Test Restaurant',
            cost_for_two=500.00,
            rating=4.5,
            location='Test Location',
            address='Test Address',
            timings='9 AM - 10 PM',
            dietary_preference='veg'
        )

    def test_restaurant_creation(self):
        """Testing that a restaurant is created successfully."""
        self.assertIsInstance(self.restaurant, Restaurant)
        self.assertEqual(self.restaurant.title, 'Test Restaurant')

    def test_str_method(self):
        """Testing the string representation of the restaurant from magic method."""
        self.assertEqual(str(self.restaurant), 'Test Restaurant')

class RestaurantPhotoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='owner', password='password123')
        self.restaurant = Restaurant.objects.create(
            owner=self.user,
            title='Test Restaurant',
            cost_for_two=500.00,
            rating=4.5,
            location='Test Location',
            address='Test Address',
            timings='9 AM - 10 PM',
            dietary_preference='veg'
        )
        self.photo = RestaurantPhoto.objects.create(
            restaurant=self.restaurant,
            image='test_image.jpg',
            description='A lovely view'
        )

    def test_photo_creation(self):
        """Testing that a restaurant photo is created successfully."""
        self.assertIsInstance(self.photo, RestaurantPhoto)

    def test_str_method(self):
        """Test the string representation of the restaurant photo."""
        self.assertEqual(str(self.photo), f'Photo of {self.restaurant.title}')

class DishModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='owner', password='password123')
        self.restaurant = Restaurant.objects.create(
            owner=self.user,
            title='Test Restaurant',
            cost_for_two=500.00,
            rating=4.5,
            location='Test Location',
            address='Test Address',
            timings='9 AM - 10 PM',
            dietary_preference='veg'
        )
        self.dish = Dish.objects.create(
            name='Test Dish',
            restaurant=self.restaurant,
            price=150.00,
            is_veg=True,
            cuisine_type='NI'
        )

    def test_dish_creation(self):
        """Testing that a dish is created successfully."""
        self.assertIsInstance(self.dish, Dish)

    def test_str_method(self):
        """Testing the string representation of the dish."""
        self.assertEqual(str(self.dish), f'Test Dish of {self.restaurant.title}')

class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='owner', password='password123')
        self.restaurant = Restaurant.objects.create(
            owner=self.user,
            title='Test Restaurant',
            cost_for_two=500.00,
            rating=4.5,
            location='Test Location',
            address='Test Address',
            timings='9 AM - 10 PM',
            dietary_preference='veg'    
        )
        self.review = Review.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            rating=4.0,
            comment='Great food!'
        )

    def test_rating_rounding(self):
        """Testing that the restaurant's rating is rounded to one decimal place."""
        
        Review.objects.create(user=self.user, restaurant=self.restaurant, rating=4.5, comment='Great food!')

        self.restaurant.update_rating()
        self.assertEqual(self.restaurant.rating, 4.2)  # (4.0 + 4.5)/2 = 4.25 => Rounds to 4.2

    
        Review.objects.create(user=self.user, restaurant=self.restaurant, rating=4.9, comment='Delicious!')
    
    
        self.restaurant.update_rating()
        self.assertEqual(self.restaurant.rating, 4.5) #(4.0 + 4.5 + 4.9) / 3 = 4.4667 => Rounds to 4.5 

    
        Review.objects.create(user=self.user, restaurant=self.restaurant, rating=4.4, comment='Tasty!')
        
        self.restaurant.update_rating()
        self.assertEqual(self.restaurant.rating, 4.5) #(4.0 + 4.5 + 4.9 + 4.4) / 4 = 4.45 => Rounds to 4.5

    def test_review_creation(self):
        """Testing that a review is created successfully."""
        self.assertIsInstance(self.review, Review)

    def test_review_update_rating(self):
        """Testing that updating a review updates the restaurant's rating."""
        self.review.rating = 5.0
        self.review.save()
        self.restaurant.update_rating()
        self.assertEqual(self.restaurant.rating, 5.0)

    def test_rating_does_not_exceed_five(self):
        """Testing that the review rating must be between 1.0 and 5.0."""
        review = Review(user=self.user, restaurant=self.restaurant, rating=6.0, comment='Test rating that exceeds 5.0')
        with self.assertRaises(ValidationError):
            review.full_clean()

    

class VisitedRestaurantModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='owner', password='password123')
        self.restaurant = Restaurant.objects.create(
            owner=self.user,
            title='Test Restaurant',
            cost_for_two=500.00,
            rating=4.5,
            location='Test Location',
            address='Test Address',
            timings='9 AM - 10 PM',
            dietary_preference='veg'
        )
        self.visit = VisitedRestaurant.objects.create(user=self.user, restaurant=self.restaurant)

    def test_visit_creation(self):
        """Testing that a visited restaurant can be recorded."""
        self.assertIsInstance(self.visit, VisitedRestaurant)

    def test_str_method(self):
        """Testing the string representation of the visited restaurant."""
        self.assertEqual(str(self.visit), f'{self.user.username} - {self.restaurant.title}')

class BookmarkedRestaurantModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='owner', password='password123')
        self.restaurant = Restaurant.objects.create(
            owner=self.user,
            title='Test Restaurant',
            cost_for_two=500.00,
            rating=4.5,
            location='Test Location',
            address='Test Address',
            timings='9 AM - 10 PM',
            dietary_preference='veg'
        )
        self.bookmark = BookmarkedRestaurant.objects.create(user=self.user, restaurant=self.restaurant)

    def test_bookmark_creation(self):
        """Testing that a restaurant can be bookmarked successfully."""
        self.assertIsInstance(self.bookmark, BookmarkedRestaurant)

    def test_str_method(self):
        """Testing the string representation of the bookmarked restaurant."""
        self.assertEqual(str(self.bookmark), f'{self.user.username} - {self.restaurant.title}')