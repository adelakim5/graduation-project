# context_processors.py
from .cart import Cart

def cart(request):
    cart = Cart(request)
    return {'cart':cart}
