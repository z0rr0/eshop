from accounts.forms import Profile, Registration
from accounts.models import Customer
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from shop import addons
from shop.cart import Cart
import logging


LOGGER = logging.getLogger(__name__)


@addons.secure
def login(request):
    # use custom wrapper method to control addons.secure
    if request.user.is_authenticated():
        return redirect(reverse('index'))
    return auth_views.login(request)


@addons.secure
@login_required
def profile(request):
    if not hasattr(request.user, 'customer'):
        LOGGER.error("user is not related with a customer")
        raise Http404("user is not related with a customer")
    cart = Cart(request)
    context = {
        'customer': request.user.customer,
        'cart_count': cart.count(),
    }
    return render(request, 'accounts/profile.html', context)


@addons.secure
@login_required
@csrf_protect
def update(request):
    """User profile update"""
    if not hasattr(request.user, 'customer'):
        raise Http404("user is not related with a customer")
    customer = request.user.customer
    if request.method == 'POST':
        form = Profile(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            with transaction.atomic():
                user = customer.user
                user.first_name = data['first_name']
                user.last_name = data['last_name']
                user.email = user.username = data['email']
                user.save()
                customer.patronymic = data['middle_name']
                customer.phone = data['phone']
                customer.save()
            return redirect(reverse('profile'))
    else:
        data = {
            'first_name': customer.user.first_name,
            'middle_name': customer.patronymic,
            'last_name': customer.user.last_name,
            'email': customer.user.email,
            'phone': customer.phone,
        }
        form = Profile(data)
    cart = Cart(request)
    context = {
        'customer': request.user.customer,
        'form': form,
        'cart_count': cart.count(),
    }
    return render(request, 'accounts/update.html', context)


@addons.secure
@csrf_protect
def registration(request):
    """User registration"""
    if request.user.is_authenticated():
        return redirect(reverse('index'))
    if request.method == 'POST':
        form = Registration(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            with transaction.atomic():
                user = User(
                    username=data['email'],
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    email=data['email'],
                )
                user.set_password(data['password'])
                user.save()
                customer = Customer(
                    user=user,
                    phone=data['phone'],
                    patronymic=data['middle_name'],
                )
                customer.save()
            return redirect(reverse('profile'))
    else:
        form = Registration()
    cart = Cart(request)
    context = {
        'form': form,
        'cart_count': cart.count(),
    }
    return render(request, 'accounts/create.html', context)
