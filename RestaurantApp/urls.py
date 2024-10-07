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

    path('', views.HomeView.as_view(), name='home'),

    path('restaurants/', views.RestaurantListView.as_view(), name='restaurant-list'),
    path('restaurants/<int:pk>/', views.RestaurantDetailView.as_view(), name='restaurant-detail'),
    path('restaurants/<int:id>/review/', views.ReviewCreateView.as_view(), name='add-review'),
    path('restaurants/<int:restaurant_id>/bookmark/', views.bookmark_restaurant, name='bookmark-restaurant'),
    path('bookmarked-restaurants/', views.bookmarked_restaurants, name='bookmarked-restaurants'),
    path('rm-bookmark/<int:bookmark_id>/', views.remove_bookmark, name='remove-bookmark'),

    path('admin/', admin.site.urls),
]

if settings.DEBUG:  # Only serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
