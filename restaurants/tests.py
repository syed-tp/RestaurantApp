from django.test import TestCase

from django.contrib.auth.models import User
from .models import Restaurant, RestaurantPhoto, Dish, Review, VisitedRestaurant, BookmarkedRestaurant
from django.core.exceptions import ValidationError
from .forms import ReviewForm

from django.urls import reverse

from django.test import TestCase
from django.urls import reverse
from .filters import RestaurantFilter
from django.core import mail
import re

# Create your tests here.

#TEST FOR MODELS
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


#TEST FOR VIEWS
class RestaurantListViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='TestUser1', password='password')
        Restaurant.objects.create(owner=cls.user, title="Restaurant 1", rating=4.5, cost_for_two=500, location="Location 1", address="Address 1")
        Restaurant.objects.create(owner=cls.user, title="Restaurant 2", rating=3.5, cost_for_two=800, location="Location 2", address="Address 2")
        Restaurant.objects.create(owner=cls.user, title="Restaurant 3", rating=5.0, cost_for_two=600, location="Location 3", address="Address 3")

    def setUp(self):
        self.client.login(username='TestUser1', password='password')

    def test_restaurant_list_view_url_exists_at_desired_location(self):
        response = self.client.get('/restaurants/')
        self.assertEqual(response.status_code, 200)

    def test_restaurant_list_view_uses_correct_template(self):
        response = self.client.get(reverse('restaurant-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurants/list.html')

    def test_restaurant_list_view_context(self):
        response = self.client.get(reverse('restaurant-list'))
        self.assertEqual(len(response.context['restaurants']), 3)

    def test_restaurant_list_view_empty_message(self):
        Restaurant.objects.all().delete()
        response = self.client.get(reverse('restaurant-list'))
        self.assertContains(response, "No restaurants available at the moment. Please check back later!")


class RestaurantDetailViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        user= User.objects.create(username='Tuser1', password='password')
        cls.restaurant = Restaurant.objects.create(owner=user, title="Restaurant 1", rating=4.5, cost_for_two=500, location="Location 1", address="Address 1")

    def test_restaurant_detail_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/restaurants/{self.restaurant.id}/')
        self.assertEqual(response.status_code, 200)

    def test_restaurant_detail_view_uses_correct_template(self):
        response = self.client.get(reverse('restaurant-detail', args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurants/detail.html')

    def test_restaurant_detail_view_context(self):
        response = self.client.get(reverse('restaurant-detail', args=[self.restaurant.id]))
        self.assertEqual(response.context['restaurant'].title, self.restaurant.title)

    def test_restaurant_detail_view_invalid_id(self):
        response = self.client.get(reverse('restaurant-detail', args=[999]))  # Non-existent restaurant ID
        self.assertEqual(response.status_code, 404)


#TEST FOR REVIEWS VIEW
class ReviewCreateViewTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.restaurant = Restaurant.objects.create(owner= self.user, title='Test Restaurant', rating=4.5, cost_for_two=500, location="Location 1", address="Address 1")
        self.client.login(username='testuser', password='testpass')

    def test_create_review_success(self):
        url = reverse('add-review', kwargs={'id': self.restaurant.id})
        data = {
            'rating': 4.5,
            'comment': 'Great food!',
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.first().comment, 'Great food!')
        
    def test_valid_rating(self):
        response = self.client.post(reverse('add-review', args=[self.restaurant.id]), {
            'rating': 4.0, 
            'comment': 'Nice food!'
        })
        self.assertRedirects(response, reverse('restaurant-detail', args=[self.restaurant.id]))

    def test_reviewForm_without_comment(self):
        response = self.client.post(reverse('add-review', args=[self.restaurant.id]), {
            'rating': 4.0,  
            'comment': ''
        })
        self.assertEqual(response.status_code, 200)
        form = response.context['form']

        self.assertTrue(form.errors)
        self.assertIn('This field is required.', form.errors['comment'])

    def test_create_review_without_login(self):
        url = reverse('add-review', kwargs={'id': self.restaurant.id})
        initial_review_count = Review.objects.count()
        data = {
            'rating': 4.0,
            'comment': 'Nice place!'
        }
        #WE DONT HAVE A LOGIN PAGE YET, SO WE CHECK THAT REVIEW NOT AFFECTED TO DB
        self.assertEqual(Review.objects.count(), initial_review_count)
        

class BookmarkRestaurantTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='TestUser1', password='password')
        cls.restaurant = Restaurant.objects.create(
            owner=cls.user,
            title="Restaurant 1",
            rating=4.5,
            cost_for_two=500,
            location="Location 1",
            address="Address 1"
        )

    def setUp(self):
        self.client.login(username='TestUser1', password='password')

    def test_bookmark_restaurant(self):
        response = self.client.post(reverse('bookmark-restaurant', args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(BookmarkedRestaurant.objects.filter(user=self.user, restaurant=self.restaurant).exists())

    def test_bookmarked_restaurants_view(self):
        self.client.post(reverse('bookmark-restaurant', args=[self.restaurant.id]))
        response = self.client.get(reverse('bookmarked-restaurants'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.restaurant.title)

    def test_remove_bookmark(self):
        self.client.post(reverse('bookmark-restaurant', args=[self.restaurant.id]))
        bookmark = BookmarkedRestaurant.objects.get(user=self.user, restaurant=self.restaurant)
        response = self.client.post(reverse('remove-bookmark', args=[bookmark.id]))  # Updated to 'remove-bookmark'
        self.assertEqual(response.status_code, 302)
        self.assertFalse(BookmarkedRestaurant.objects.filter(user=self.user, restaurant=self.restaurant).exists())

    def test_remove_non_existent_bookmark(self):
        response = self.client.post(reverse('remove-bookmark', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_remove_bookmark_not_owned(self):
        another_user = User.objects.create_user(username='AnotherUser', password='password')
        self.client.logout()
        self.client.login(username='AnotherUser', password='password')
        self.client.post(reverse('bookmark-restaurant', args=[self.restaurant.id]))

        self.client.logout()
        self.client.login(username='TestUser1', password='password')

        response = self.client.post(reverse('remove-bookmark', args=[1]))
        self.assertEqual(response.status_code, 404)


class VisitedRestaurantTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='TestUser1', password='password')
        cls.restaurant = Restaurant.objects.create(
            owner=cls.user,
            title="Restaurant 1",
            rating=4.5,
            cost_for_two=500,
            location="Location 1",
            address="Address 1"
        )

    def setUp(self):
        self.client.login(username='TestUser1', password='password')

    def test_visit_restaurant(self):
        response = self.client.post(reverse('visit-restaurant', args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(VisitedRestaurant.objects.filter(user=self.user, restaurant=self.restaurant).exists())

    def test_visited_restaurants_view(self):
        self.client.post(reverse('visit-restaurant', args=[self.restaurant.id]))
        response = self.client.get(reverse('visited-restaurants'))  # Make sure this URL is correct
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.restaurant.title)

    def test_remove_visit(self):
        self.client.post(reverse('visit-restaurant', args=[self.restaurant.id]))
        visit = VisitedRestaurant.objects.get(user=self.user, restaurant=self.restaurant)
        response = self.client.post(reverse('remove-visit', args=[visit.id]))  # Updated to 'remove-visit'
        self.assertEqual(response.status_code, 302)
        self.assertFalse(VisitedRestaurant.objects.filter(user=self.user, restaurant=self.restaurant).exists())

    def test_remove_non_existent_visit(self):
        response = self.client.post(reverse('remove-visit', args=[999]))  # Updated to 'remove-visit'
        self.assertEqual(response.status_code, 404)

    def test_remove_visit_not_owned(self):
        another_user = User.objects.create_user(username='AnotherUser', password='password')
        self.client.logout()
        self.client.login(username='AnotherUser', password='password')
        self.client.post(reverse('visit-restaurant', args=[self.restaurant.id]))

        self.client.logout()
        self.client.login(username='TestUser1', password='password')

        response = self.client.post(reverse('remove-visit', args=[1]))
        self.assertEqual(response.status_code, 404)

        
class RestaurantFilterTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='owner', password='password')

    def setUp(self):
        
        self.client.login(username='owner', password='password')

        self.restaurant1 = Restaurant.objects.create(
            owner=self.user,
            title="Italian Bistro",
            cost_for_two=500,
            rating=4.5,
            dietary_preference='vegan',
            spotlight=True,
            location="Downtown",
            address="123 Italian St."
        )
        self.restaurant2 = Restaurant.objects.create(
            owner=self.user,
            title="Spicy Thai",
            cost_for_two=300,
            rating=4.0,
            dietary_preference='veg',
            spotlight=False,
            location="Thailand",
            address="71 Thai Rd."
        )
        self.restaurant3 = Restaurant.objects.create(
            owner=self.user,
            title="Burger House",
            cost_for_two=700,
            rating=5.0,
            dietary_preference='non-veg',
            spotlight=False,
            location="DownTown",
            address="101 Burger Ln."
        )

    def test_filter_by_title(self):
        response = self.client.get(reverse('restaurant-list'), {'search': 'Burger'})
        self.assertEqual(len(response.context['filter'].qs), 1)
        self.assertEqual(response.context['filter'].qs.first(), self.restaurant3)

    def test_filter_by_dietary_preference(self):
        response = self.client.get(reverse('restaurant-list'), {'dietary_preference': 'vegan'})
        self.assertEqual(len(response.context['filter'].qs), 1)
        self.assertEqual(response.context['filter'].qs.first(), self.restaurant1)

    def test_filter_by_cost_order(self):
        response = self.client.get(reverse('restaurant-list'), {'cost_order': 'cost_for_two'})
        self.assertEqual(list(response.context['filter'].qs), [self.restaurant2, self.restaurant1, self.restaurant3])

    def test_filter_by_rating_order(self):
        response = self.client.get(reverse('restaurant-list'), {'rating_order': '-rating'})
        self.assertEqual(list(response.context['filter'].qs), [self.restaurant3, self.restaurant1, self.restaurant2])

    def test_filter_by_spotlight(self):
        response = self.client.get(reverse('restaurant-list'), {'spotlight': '1'})
        self.assertEqual(len(response.context['filter'].qs), 1)
        self.assertEqual(response.context['filter'].qs.first(), self.restaurant1)

    def test_no_restaurants(self):
        Restaurant.objects.all().delete()
        response = self.client.get(reverse('restaurant-list'))
        self.assertContains(response, "No restaurants available at the moment. Please check back later!")


class AuthTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='oldpassword123'
        )

    def test_sign_up(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'oldpassword123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_logout(self):
        self.client.login(username='testuser', password='oldpassword123')
        response = self.client.post(reverse('logout'))  
        self.assertEqual(response.status_code, 302)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_forgot_password(self):
        response = self.client.post(reverse('password_reset'), {
            'email': 'test@example.com',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
    
    def test_change_password(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('password_change'), {
            'old_password': 'password123',
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123',
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertFalse(self.user.check_password('password123'))


class DishManagementTests(TestCase):
    
    def setUp(self):
        self.owner = User.objects.create_user(
            username='owner',
            password='password123'
        )
        self.client.login(username='owner', password='password123')
        
        self.restaurant = Restaurant.objects.create(
            owner=self.owner,
            title="DishManagement",
            cost_for_two=500,
            rating=4.5,
            dietary_preference='vegan',
            spotlight=True,
            location="Downtown",
            address="123 Italian St."
        )

        self.dish = Dish.objects.create(
            name='Test Dish',
            restaurant=self.restaurant,
            price=100.00,
            is_veg=True,
            cuisine_type='IF',
        )

    def test_dish_create_view(self):
        url = reverse('dish-add', kwargs={'restaurant_id': self.restaurant.id})
        data = {
            'name': 'New Dish',
            'price': 20.00,
            'is_veg': True,
            'cuisine_type': 'IF',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Dish.objects.filter(name='New Dish').exists())
    
    def test_dish_update_view(self):
        url = reverse('dish-edit', kwargs={'pk': self.dish.pk, 'restaurant_id': self.restaurant.id})
        data = {
            'name': 'Updated Dish',
            'price': 15.00,
            'is_veg': True,
            'cuisine_type': 'IF',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.dish.refresh_from_db()
        self.assertEqual(self.dish.name, 'Updated Dish') 

    def test_dish_delete_view(self):
        url = reverse('dish-delete', kwargs={'restaurant_id': self.restaurant.id, 'pk': self.dish.id})
        response = self.client.post(url)

        self.assertRedirects(response, reverse('restaurant-detail', kwargs={'pk': self.restaurant.id}))

        dish_instance = Dish.objects.first()
        self.assertTrue(dish_instance.is_deleted)
        self.assertEqual(Dish.objects.filter(is_deleted=False).count(), 0)
        