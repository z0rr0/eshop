from django.shortcuts import render
from .models import Category
from shop import addons


@addons.secure
def index(request):
    categories = Category.objects.all().order_by('id')
    context = {
        'categories': categories,
        'request': request,
    }
    return render(request, 'sales/index.html', context)
