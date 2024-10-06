from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect

from django.views.generic import TemplateView, ListView, DetailView
from .models import Restaurant, RestaurantPhoto, Dish, Review, BookmarkedRestaurant

from django.core.paginator import Paginator

from django.views.generic.edit import CreateView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ReviewForm

from django.contrib.auth.decorators import login_required

from .filters import RestaurantFilter, DishFilter

# Create your views here.


class HomeView(TemplateView):
    template_name ='home.html'


class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'restaurants/list.html'
    context_object_name = 'restaurants'
    paginate_by = 10
    filterset_class = RestaurantFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = RestaurantFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        context['bookmarked_restaurants'] = BookmarkedRestaurant.objects.filter(user=self.request.user).values_list('restaurant_id', flat=True)
        return context
    

class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'restaurants/detail.html'
    context_object_name = 'restaurant'
    filterset_class = DishFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant = self.object
        menu_items = restaurant.menu_items.filter(is_deleted=False)
        self.filterset = self.filterset_class(self.request.GET, queryset=menu_items)
        context['menu_items'] = self.filterset.qs
        context['filter'] = self.filterset
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
        form.instance.restaurant = self.restaurant
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['restaurant'] = self.restaurant
        return context

    def get_success_url(self):
        return reverse('restaurant-detail', kwargs={'pk': self.restaurant.pk})
    

@login_required
def bookmark_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    BookmarkedRestaurant.objects.get_or_create(user=request.user, restaurant=restaurant)
    return redirect('restaurant-list'   )

@login_required
def bookmarked_restaurants(request):
    bookmarks = BookmarkedRestaurant.objects.filter(user=request.user)
    return render(request, 'restaurants/bookmarked.html', {'bookmarks': bookmarks})

@login_required
def remove_bookmark(request, bookmark_id):
    bookmark = get_object_or_404(BookmarkedRestaurant, id=bookmark_id, user=request.user)
    bookmark.delete()
    return redirect('bookmarked-restaurants')