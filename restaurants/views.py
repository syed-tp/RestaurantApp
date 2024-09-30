from django.shortcuts import render

from django.views.generic import TemplateView, ListView, DetailView
from .models import Restaurant, RestaurantPhoto, Dish   

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
    template_name = 'restaurants/detail.html'
    context_object_name = 'restaurant'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu_items"] = self.object.menu_items.filter(is_deleted=False) 
        return context
    
   
    