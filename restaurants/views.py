from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from django.views.generic import TemplateView, ListView, DetailView
from .models import Restaurant, RestaurantPhoto, Dish, Review, BookmarkedRestaurant

from django.core.paginator import Paginator

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ReviewForm, SignUpForm

from django.contrib.auth.decorators import login_required

from .filters import RestaurantFilter, DishFilter

from django.utils.decorators import method_decorator
from .decorators import restaurant_owner_required 
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
        queryset = super().get_queryset().order_by('id')
        self.filterset = RestaurantFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        if self.request.user.is_authenticated:
            context['bookmarked_restaurants'] = BookmarkedRestaurant.objects.filter(user=self.request.user).values_list('restaurant_id', flat=True)
        else:
            context['bookmarked_restaurants'] = []
        return context
    

class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'restaurants/detail.html'
    context_object_name = 'restaurant'
    filterset_class = DishFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant = self.object
        context['is_owner'] = restaurant.owner == self.request.user
        menu_items = restaurant.menu_items.filter(is_deleted=False)
        self.filterset = self.filterset_class(self.request.GET, queryset=menu_items)
        context['menu_items'] = self.filterset.qs
        context['filter'] = self.filterset
        context['reviews'] = restaurant.reviews.order_by('-id')  
        return context


class DishCreateView(CreateView):
    model = Dish
    fields = ['name', 'price', 'is_veg', 'image', 'cuisine_type']
    template_name = 'restaurants/dish_form.html'

    @method_decorator(restaurant_owner_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Add'
        return context

    def form_valid(self, form):
        restaurant = get_object_or_404(Restaurant, pk=self.kwargs['restaurant_id'])
        form.instance.restaurant = restaurant
        return super().form_valid(form)
        
    def get_success_url(self):
        return reverse_lazy('restaurant-detail', kwargs={'pk': self.object.restaurant.pk})


class DishUpdateView(UpdateView):
    model = Dish
    fields = ['name', 'price', 'is_veg', 'image', 'cuisine_type']
    template_name = 'restaurants/dish_form.html'

    @method_decorator(restaurant_owner_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Edit'
        return context

    def get_queryset(self):
        restaurant = get_object_or_404(Restaurant, pk=self.kwargs['restaurant_id'])
        return restaurant.menu_items.all()
    
    def get_success_url(self):
        return reverse_lazy('restaurant-detail', kwargs={'pk': self.object.restaurant.pk})


class DishDeleteView(DeleteView):
    model = Dish
    template_name = 'restaurants/dish_confirm_delete.html'

    @method_decorator(restaurant_owner_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        restaurant = get_object_or_404(Restaurant, pk=self.kwargs['restaurant_id'])
        return restaurant.menu_items.all()
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('restaurant-detail', kwargs={'pk': self.object.restaurant.pk})
 

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
    
    
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

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