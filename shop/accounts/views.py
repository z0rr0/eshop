from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render, redirect
from shop import addons
from accounts.forms import Profile
import logging


LOGGER = logging.getLogger(__name__)


@addons.secure
def login(request):
    # use custom wrapper method to control addons.secure
    return auth_views.login(request)


@login_required
@addons.secure
def profile(request):
    if not hasattr(request.user, 'customer'):
        LOGGER.error("user is not related with a customer")
        raise Http404("user is not related with a customer")
    context = {
        'customer': request.user.customer,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
@addons.secure
@csrf_protect
def update(request):
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
    context = {
        'customer': request.user.customer,
        'form': form,
    }
    return render(request, 'accounts/update.html', context)
