from decimal import Decimal

from shop.models import ProductProxy


class Cart():
    def __init__(self, request) -> None:
        """
        Initialize the Cart object.

        Parameters:
        - request: The request object containing session information.

        This method initializes the Cart object with the session information from the request.
        If the 'session_key' is not present in the session, it creates an empty dictionary for the cart.
        """
        self.session = request.session

        cart = self.session.get('session_key')

        if not cart:
            cart = self.session['session_key'] = {}
        self.cart = cart

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1):
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': quantity, 'price': str(product.price)}
        else:
            self.cart[product_id]['quantity'] += quantity
            self.cart[product_id]['price'] = str(product.price) * self.cart[product_id]['quantity']
            self.session.modified = True

