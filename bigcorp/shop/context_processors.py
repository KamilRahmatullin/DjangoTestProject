from django.shortcuts import render

from .models import Category, ProductProxy


def categories(request):
    """
    Returns a list of all categories.
    """
    categories = Category.objects.filter(parent=None)
    return {'categories': categories}
