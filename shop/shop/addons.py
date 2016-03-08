from django.shortcuts import redirect


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


def easy_cache(cache):
    def get(func):
        def wrapper(*args, **kwargs):
            value = cache.get(args[0])
            if value is not None:
                return value
            value = func(*args, **kwargs)
            cache[args[0]] = value
            return value
        return wrapper
    return get
