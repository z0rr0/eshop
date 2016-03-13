from django.shortcuts import redirect
from django.contrib.auth.models import User


class EmailAuthBackend(object):
    """
    Email Authentication Backend

    Allows a user to sign in using an email/password pair.
    """

    def authenticate(self, username=None, password=None):
        """ Authenticate a user based on email address as the user name. """
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        """ Get a User object from the user_id."""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def get_path(request, secure):
    """get_path returns full URL path"""
    uri = request.get_host() + request.get_full_path()
    if secure:
        uri = "https://" + uri
    else:
        uri = "http://" + uri
    return uri


def secure(func):
    """decorator for redirect http->https"""
    def wrapper(*args, **kwargs):
        request = args[0]
        if not request.is_secure():
            return redirect(get_path(request, True))
        else:
            return func(*args, **kwargs)
    return wrapper


def nosecure(func):
    """decorator for redirect https->http"""
    def wrapper(*args, **kwargs):
        request = args[0]
        if request.is_secure():
            return redirect(get_path(request, False))
        else:
            return func(*args, **kwargs)
    return wrapper
