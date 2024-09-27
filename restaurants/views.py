from django.shortcuts import render

from django.views.generic import TemplateView, ListView, DetailView
from .models import Restaurant, RestaurantPhoto

# Create your views here.


class HomeView(TemplateView):
    template_name ='home.html'

class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'restaurants/list.html'
    context_object_name = 'restaurants'
    paginated_by = 10

class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'resturants/detail.html'
    context_object_name = 'restaurants'
