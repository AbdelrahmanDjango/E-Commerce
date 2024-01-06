from .cart import Cart
def cart(request):
    return {'cart': Cart(request)}
#'cart' => any name you want.