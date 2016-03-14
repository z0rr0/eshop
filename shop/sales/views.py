from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db import transaction
from django.forms import formset_factory
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect
from sales.forms import OrderForm, DeliveryForm
from sales.models import Category, Product, Order, ProductSet
from accounts.models import Delivery
from shop import addons
from shop.cart import Cart
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
    return cart.set(render(request, 'sales/show.html', context))


@addons.nosecure
def delete(request, id):
    """It removes the product from the Cart"""
    product = get_object_or_404(Product, pk=id)
    cart = Cart(request)
    cart.delete(product)
    return cart.set(redirect(reverse('cart')))


@addons.secure
@csrf_protect
def cart(request):
    """It showes customer's cart
    and allows to change products numbers.
    """
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
    return cart.set(render(request, 'sales/cart.html', context))


@addons.secure
@login_required
@csrf_protect
def confirm(request):
    """It confirms a customer's order
    and sets delivery address
    """
    if not hasattr(request.user, 'customer'):
        raise Http404("user is not related with a customer")
    customer = request.user.customer
    cart = Cart(request)
    if cart.is_empty():
        # empty cart can't approve any order
        return redirect(reverse('index'))
    products = []
    try:
        for product, count in cart.get().items():
            product.count = count
            product.total = round(product.price * int(count), 2)
            products.append(product)
    except (ValueError,) as err:
        raise Http404(err)
    if request.method == 'POST':
        form = DeliveryForm(request.POST)
        form.set_choises(customer)
        if form.is_valid():
            data = form.cleaned_data
            with transaction.atomic():
                if data['new']:
                    # create new delivery address
                    delivery = Delivery(
                        customer=customer,
                        address=data['new'],
                    )
                    delivery.save()
                else:
                    # use existed address
                    delivery = get_object_or_404(Delivery, pk=data['existed'])
                order = Order(
                    customer=customer,
                    desc=data['comment'],
                )
                order.save()
                for product in products:
                    ProductSet.objects.create(
                        product=product,
                        order=order,
                        number=product.count,
                    )
            return cart.clean(redirect(reverse('index')))
    else:
        form = DeliveryForm()
        form.set_choises(customer)
    context = {
        'products': products,
        'cart_count': cart.count(),
        'total': cart.total(),
        'form': form,
    }
    return render(request, 'sales/confirm.html', context)


@addons.secure
@login_required
def orders(request):
    if not hasattr(request.user, 'customer'):
        raise Http404("user is not related with a customer")
    cart = Cart(request)
    orders = request.user.customer.order_set.all()
    context = {
        'orders': orders,
        'cart_count': cart.count(),
    }
    return render(request, 'sales/orders.html', context)


@addons.secure
@login_required
def order(request, id):
    if not hasattr(request.user, 'customer'):
        raise Http404("user is not related with a customer")
    cart = Cart(request)
    order = get_object_or_404(Order, pk=id)
    context = {
        'order': order,
        'cart_count': cart.count(),
    }
    return render(request, 'sales/order.html', context)
