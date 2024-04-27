from decimal import Decimal

from shop.models import ProductProxy


class Cart():
    def __init__(self, request) -> None:
        self.session = request.session
