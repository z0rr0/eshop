from django.conf import settings
from django.shortcuts import get_object_or_404
from sales.models import Product
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
                product = get_object_or_404(Product, pk=product_id)
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
        return response

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

    def clean(self, response):
        response.delete_cookie(self.NAME)
        return response