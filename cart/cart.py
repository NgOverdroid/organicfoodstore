from store.models import Product
from accounts.models import Profile
class Cart:
    def __init__(self, request):
        self.session = request.session
        #Get request
        self.request = request
        #Get the current session key if it exists
        cart = self.session.get('session_key')
        #If the user is new, no session -> create one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {} #Chain assignment, answers needed

        #Make cart available on all sites
        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        product_quantity = str(quantity)
        # do nothing if the product is already in the cart, else add the product to the cart
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_quantity)
        self.session.modified = True
        
        #Deal with logged in user
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            #conver dict {'3':2} into json file, which uses " => {"3":2}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            #update the old_cart field in the Profile model with carty
            current_user.update(old_cart=str(carty))

    def get_products(self):
        product_ids = self.cart.keys() #get ids from cart
        products = Product.objects.filter(id__in = product_ids) #use ids to lookup products in the database
        return products
    
    def get_quantities(self):
        quantities = self.cart
        return quantities
    
    def total(self):
        product_ids = self.cart.keys() #Get keys in cart, the keys are the ids
        products = Product.objects.filter(id__in = product_ids) #Get all products based on keys in cart
        quantities = self.cart
        small_sum = 0
        big_sum = 0 
        dict_sum = {}
        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key: 
                    small_sum = int(product.price) * value
                    big_sum = big_sum + (int(product.price) * value)
                    dict_sum[f'{product.id}'] = small_sum        
        dict_sum['big_sum'] = big_sum

        return dict_sum
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        #Get cart
        ourcart = self.cart
        #Update cart
        ourcart[product_id] = product_qty
        self.session.modified = True

        #Deal with logged in user
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            #conver dict {'3':2} into json file, which uses " => {"3":2}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            #update the old_cart field in the Profile model with carty
            current_user.update(old_cart=str(carty))
        
        thing = self.cart
        return thing

    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            #conver dict {'3':2} into json file, which uses " => {"3":2}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            #update the old_cart field in the Profile model with carty
            current_user.update(old_cart=str(carty))
    
    def re_add(self, product, quantity):
        product_id = str(product)
        product_quantity = str(quantity)
        # do nothing if the product is already in the cart, else add the product to the cart
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_quantity)
        self.session.modified = True

        #Deal with logged in user
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id = self.request.user.id)
            #conver dict {'3':2} into json file, which uses " => {"3":2}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            #update the old_cart field in the Profile model with carty
            current_user.update(old_cart=str(carty))