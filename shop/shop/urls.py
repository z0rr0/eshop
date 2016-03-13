"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
import sales.views as sales
import accounts.views as accounts
from django.contrib.auth import views as auth_views

# error pages
handler500 = "sales.views.custom_500"
handler404 = "sales.views.custom_404"

urlpatterns = [
    url(r'^$', sales.index, name='index'),
    # account service pages
    url(r'^login/?$', accounts.login, name='login'),
    url(r'^logout/?$', auth_views.logout, {'next_page': '/'}, name='logout'),
    # also neede password_reset + password_change

    url(r'^profile/?$', accounts.profile, name='profile'),
    url(r'^profile/update/?$', accounts.update, name='profile_update'),
    url(r'^registration/?$', accounts.registration, name='registration'),

    url(r'^show/(?P<id>\d+)/?$', sales.show, name='show'),
    url(r'^add/(?P<id>\d+)/?$', sales.add, name='add'),
    url(r'^delete/(?P<id>\d+)/?$', sales.delete, name='delete'),
    url(r'^cart/?$', sales.cart, name='cart'),

    # admin interface
    url(r'^admin/', admin.site.urls),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
]
