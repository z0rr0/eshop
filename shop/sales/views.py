from django.shortcuts import render
from .models import Category
from shop import addons
import logging


LOGGER = logging.getLogger(__name__)


@addons.nosecure
def index(request):
    LOGGER.info('index')
    categories = Category.objects.all().order_by('id')
    context = {
        'categories': categories,
        'request': request,
    }
    return render(request, 'sales/index.html', context)
