from django.shortcuts import render
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.http import Http404
from shop import addons
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
def update(request):
    if not hasattr(request.user, 'customer'):
        raise Http404("user is not related with a customer")
    customer = request.user.customer

