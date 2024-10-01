from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404

from django.views.generic import TemplateView, ListView, DetailView
from .models import Restaurant, RestaurantPhoto, Dish, Review

from django.core.paginator import Paginator

from django.views.generic.edit import CreateView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ReviewForm

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
    

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'restaurants/review_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.restaurant = get_object_or_404(Restaurant, pk=self.kwargs['id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form): 
        form.instance.user = self.request.user
        form.instance.restaurant_id = self.restaurant
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['restaurant'] = self.restaurant
        return context

    def get_success_url(self):
        return reverse('restaurant-detail', kwargs={'pk': self.restaurant.pk})
    
    
    