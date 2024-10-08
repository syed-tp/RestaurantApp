"""
URL configuration for RestaurantApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from restaurants import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('', views.HomeView.as_view(), name='home'),

    path('restaurants/', views.RestaurantListView.as_view(), name='restaurant-list'),
    path('restaurants/<int:pk>/', views.RestaurantDetailView.as_view(), name='restaurant-detail'),
    path('restaurants/<int:id>/review/', views.ReviewCreateView.as_view(), name='add-review'),


    path('restaurant/<int:restaurant_id>/dish/add/', views.DishCreateView.as_view(), name='dish-add'),
    path('restaurant/<int:restaurant_id>/dish/<int:pk>/edit/', views.DishUpdateView.as_view(), name='dish-edit'),
    path('restaurant/<int:restaurant_id>/dish/<int:pk>/delete/', views.DishDeleteView.as_view(), name='dish-delete'),

    path('restaurants/<int:restaurant_id>/bookmark/', views.bookmark_restaurant, name='bookmark-restaurant'),
    path('bookmarked-restaurants/', views.bookmarked_restaurants, name='bookmarked-restaurants'),
    path('rm-bookmark/<int:bookmark_id>/', views.remove_bookmark, name='remove-bookmark'),

    path('restaurant/<int:restaurant_id>/visit/', views.visit_restaurant, name='visit-restaurant'),
    path('visited-restaurants/', views.visited_restaurants, name='visited-restaurants'),
    path('rm-visit/<int:visit_id>/', views.remove_visit, name='remove-visit'),

    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
