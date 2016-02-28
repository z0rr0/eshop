from django.shortcuts import redirect


def get_path(request, secure):
    uri = "{}{}".format(request.get_host(), request.get_full_path())
    if secure:
        uri = "https://" + uri
    else:
        uri = "http://" + uri
    return uri


def secure(func):
    def wrapper(*args, **kwargs):
        request = args[0]
        if not request.is_secure():
            return redirect(get_path(request, True))
        else:
            return func(*args, **kwargs)
    return wrapper


def nosecure(func):
    def wrapper(*args, **kwargs):
        request = args[0]
        if request.is_secure():
            return redirect(get_path(request, False))
        else:
            return func(*args, **kwargs)
    return wrapper
