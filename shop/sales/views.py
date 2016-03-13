from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.forms import formset_factory
from django.shortcuts import render, get_object_or_404, redirect
from sales.models import Category, Product
from sales.forms import OrderForm
from django.views.decorators.csrf import csrf_protect
from shop import addons
import logging


LOGGER = logging.getLogger(__name__)


class Cart(object):
    """Customers cart

    It uses cookie NAME.
    Cookie template is "product_id1::number1;product_id2::number2".
    """

    NAME = "cart"
    SEP_NUM, SEP_PR = '::', ';'

    def __init__(self, request=None):
        super(Cart, self).__init__()
        self._request = request
        self._storage = {}

    def is_empty(self):
        if self._request is None:
            return True
        try:
            self._value = self._request.get_signed_cookie(
                self.NAME,
                None,
                settings.COOKIE_SALT,
                max_age=settings.COOKIE_EXPIRE
            )
            if not self._value:
                return True
        except KeyError:
            return True
        return False

    def get(self, force=False):
        if self._storage or self.is_empty():
            return self._storage
        try:
            value = self._request.get_signed_cookie(
                self.NAME,
                None,
                settings.COOKIE_SALT,
                max_age=settings.COOKIE_EXPIRE
            )
            for pair in value.split(self.SEP_PR):
                product_id, number = pair.split(self.SEP_NUM)
                product = Product.objects.get(pk=product_id)
                self._storage[product] = number
        except (KeyError, ValueError) as err:
            LOGGER.error(err)
        return self._storage

    def set(self, response):
        pairs = []
        for product in self._storage:
            pairs.append("{}{}{}".format(product.id, self.SEP_NUM, self._storage[product]))
        value = self.SEP_PR.join(pairs)
        response.set_signed_cookie(
            self.NAME,
            value,
            settings.COOKIE_SALT,
            max_age=settings.COOKIE_EXPIRE,
        )

    def add_or_update(self, product, number, reset=False):
        if reset:
            products = {}
        else:
            products = self.get()
        products[product] = number
        self._storage = products

    def delete(self, product):
        products = self.get()
        try:
            products.pop(product)
        except KeyError:
            LOGGER.debug("ignore missing product")
        self._storage = products

    def count(self):
        return len(self.get())

    def total(self):
        value = 0
        products = self.get()
        try:
            for product in products:
                value += product.price * int(products[product])
        except ValueError:
            return 0
        return value

    def has(self, product):
        products = self.get()
        if products.get(product):
            return True
        return False

    def clean(self):
        response.delete_cookie(self.NAME)
        return response


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

    cart = Cart(request)
    context = {
        'categories': categories,
        'request': request,
        'params': params,
        'products': products,
        'search': search,
        'category': category,
        'cart_count': cart.count(),
    }
    return render(request, 'sales/index.html', context)


def custom_500(request):
    # some custom actions
    return render(request, '500.html', {"MEDIA_URL", settings.MEDIA_URL})


def custom_404(request):
    # some custom actions
    return render(request, '404.html')


@addons.nosecure
def show(request, id):
    """Product card page"""
    product = get_object_or_404(Product, pk=id)
    cart = Cart(request)
    context = {
        'product': product,
        'in_cart': cart.has(product),
        'cart_count': cart.count(),
    }
    return render(request, 'sales/show.html', context)


@addons.nosecure
def add(request, id):
    """It adds the product to the Cart"""
    product = get_object_or_404(Product, pk=id)
    cart = Cart(request)
    cart.add_or_update(product, 1)
    context = {
        'product': product,
        'in_cart': cart.has(product),
        'cart_count': cart.count(),
    }
    response = render(request, 'sales/show.html', context)
    cart.set(response)
    return response


@addons.nosecure
def delete(request, id):
    """It removes the product from the Cart"""
    product = get_object_or_404(Product, pk=id)
    cart = Cart(request)
    cart.delete(product)
    response = redirect(reverse('cart'))
    cart.set(response)
    return response


@addons.secure
@csrf_protect
def cart(request):
    cart = Cart(request)
    products = cart.get()
    products_ids = {p.id: p for p in products}

    OrderFormSet = formset_factory(OrderForm, extra=0)
    if request.method == 'POST':
        formset = OrderFormSet(request.POST)
        if formset.is_valid() and formset.has_changed():
            for cd in formset.cleaned_data:
                product = get_object_or_404(Product, pk=cd['product'])
                cart.add_or_update(product, cd['count'])
    else:
        data = [{'product': p.id, 'count': c} for p, c in products.items()]
        formset = OrderFormSet(initial=data)
    for form in formset:
        form.product_info = products_ids[int(form.hidden_fields()[0].value())]
    context = {
        'products': products,
        'formset': formset,
        'cart_count': cart.count(),
        'total': cart.total(),
    }
    response = render(request, 'sales/cart.html', context)
    cart.set(response)
    return response
