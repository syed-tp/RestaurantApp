from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render

from django.views.generic import TemplateView, ListView, DetailView
from .models import Restaurant, RestaurantPhoto, Dish   

from django.core.paginator import Paginator

# Create your views here.


class HomeView(TemplateView):
    template_name ='home.html'

class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'restaurants/list.html'
    context_object_name = 'restaurants'
    paginate_by = 10

    def get_queryset(self):
        queryset = Restaurant.objects.all().order_by('id')
        return queryset
    
class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'restaurants/detail.html'
    context_object_name = 'restaurant'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu_items"] = self.object.menu_items.filter(is_deleted=False) 
        return context
    
   
    