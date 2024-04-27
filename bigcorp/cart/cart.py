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
        """
        Get the total number of items in the cart.

        This method calculates and returns the total quantity of items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        """
        Iterate over the items in the cart.

        This method iterates over the items in the cart and enriches each item with additional information such as the
        associated product and total price.

        Yields:
        - dict: A dictionary containing information about each item in the cart, including the associated product, price,
         quantity, and total price.

        The method first retrieves the product IDs from the cart and then fetches the corresponding products using ProductProxy.
        It then creates a copy of the cart to avoid modifying the original cart during iteration. For each product,
        it enriches the cart item with the associated product. Finally,
        it calculates the total price for each item and yields the enriched item.
        """
        product_ids = self.cart.keys()
        products = ProductProxy.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total'] = item['price'] * item['quantity']
            yield item

    def add(self, product, quantity=1):
        """
        Add a product to the cart or update its quantity.

        Parameters:
        - product: The product object to be added to the cart.
        - quantity: The quantity of the product to be added (default is 1).

        This method adds the specified product to the cart with the given quantity. If the product is already in the cart,
        the quantity is updated. The session modification flag is set to True to indicate that the session has been modified.
        """
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': quantity, 'price': str(product.price)}
        else:
            self.cart[product_id]['quantity'] = quantity
            self.cart[product_id]['price'] = str(product.price)
            self.session.modified = True

    def get_total_price(self):
        """
        Get the total price of the cart.

        This method calculates and returns the total price of all items in the cart.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())