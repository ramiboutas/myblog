from .models import BlogCategory


def categories(request):
    return {
        'all_categories': BlogCategory.objects.all(),
        'request': request
    }
