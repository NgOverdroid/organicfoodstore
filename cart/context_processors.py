from .cart import Cart
#Create context processor so cart works on all site, because we need to keep track what the user does in other sites
def cart(request):
    #Return the default data from our cart
    return {'cart': Cart(request)}