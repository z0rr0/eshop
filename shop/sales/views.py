from django.shortcuts import render
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from sales.models import Category, Product
from shop import addons
import logging


LOGGER = logging.getLogger(__name__)


@addons.nosecure
def index(request):
    on_page = 2
    categories = Category.objects.all().order_by('name')
    # filter params: page, category, name
    category = None
    params = {'cat_url': [], 'page_url': []}
    products = Product.objects.all().order_by('-modified')

    # text search filter
    search = request.GET.get('name', '')
    if search:
        products = products.filter(name__icontains=request.GET['name'])
        params['cat_url'].append('name=' + request.GET['name'])
        params['page_url'].append('name=' + request.GET['name'])

    # categories filter
    try:
        if request.GET.get('cat'):
            category = Category.objects.get(pk=int(request.GET['cat']))
            products = products.filter(category=category)
            params['page_url'].append('cat=' + str(category.id))
    except (ValueError, Category.DoesNotExist) as err:
        LOGGER.error(err)

    # pagination filter
    paginator = Paginator(products, on_page)
    page = request.GET.get('page', 1)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        products = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        products = paginator.page(page)

    params['cat_url'].append('page=' + str(page))
    context = {
        'categories': categories,
        'request': request,
        'params': params,
        'products': products,
        'search': search,
        'category': category,
    }
    return render(request, 'sales/index.html', context)


def custom_500(request):
    # some custom actions
    return render(request, '500.html', {"MEDIA_URL", settings.MEDIA_URL})


def custom_404(request):
    # some custom actions
    return render(request, '404.html')
