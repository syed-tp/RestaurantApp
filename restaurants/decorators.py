from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from .models import Restaurant

def restaurant_owner_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        restaurant = get_object_or_404(Restaurant, pk=kwargs['restaurant_id'])
        if restaurant.owner != request.user:
            return HttpResponseForbidden()
        return view_func(request, *args, **kwargs)
    return _wrapped_view
