import django_filters
from .models import Restaurant, Dish
from django.db.models import Q

class RestaurantFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_by_title_or_location', label='Search')

    cost_order = django_filters.OrderingFilter(
        fields=(
            
            ('cost_for_two', 'cost_for_two'),   
            ('-cost_for_two', 'cost_for_two_desc'),
        ),
    )
    
    rating_order = django_filters.OrderingFilter(
        fields=(
            ('rating', 'rating'),
            ('-rating', 'rating_desc'), 
        ),
    )

    dietary_preference = django_filters.ChoiceFilter(
        choices=Restaurant.DIETARY_CHOICES,
        empty_label='All dietary types'
    )

    spotlight = django_filters.BooleanFilter(widget=django_filters.widgets.BooleanWidget())

    class Meta:
        model = Restaurant
        fields = []

    def filter_by_title_or_location(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(title__icontains=value) | 
                Q(location__icontains=value)|
                Q(address__icontains=value)
            )
        return queryset


class DishFilter(django_filters.FilterSet):
    dish_search = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    cuisine_type = django_filters.ChoiceFilter(choices=Dish.CUISINE_CHOICES, empty_label="Cuisine Type")
    is_veg = django_filters.BooleanFilter(widget=django_filters.widgets.BooleanWidget())

    class Meta:
        model = Dish
        fields = []