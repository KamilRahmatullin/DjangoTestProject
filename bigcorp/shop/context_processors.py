from .models import Category


def categories(request):
    """
    Returns a list of all categories.
    """
    categories = Category.objects.filter(parent=None)
    return {'categories': categories}
