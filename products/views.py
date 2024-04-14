from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Offer, Order, Categorie, Elvis
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .forms import ElvisForm
# Create your views here.


def index(request):
    cart = request.session.get('cart')

    if not cart:
        request.session['cart'] = {}
    # products = Product.objects.all()
    categories = Categorie.objects.all()
    categorie_id = request.GET.get('categorie')
    if categorie_id:
        if categorie_id == "10":
            print("yash")
            products = Product.objects.all()
        else:
            products = Product.get_all_products_by_categorieid(categorie_id)
    else:
        products = Product.objects.all()
    data = {}
    data['products'] = products
    data['categories'] = categories
    # return HttpResponse('Hello, Welcome to the project')
    product = request.POST.get('product')
    remove = request.POST.get('remove')
    if product is not None:
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session['cart'] = cart
        print(request.session['cart'])
    return render(request, 'index.html', data)


def cart(request):
    if request.method == 'POST':
        codes = ''
        codes = request.POST.get('getcode')
        offers = Offer.objects.all()
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        return render(request, 'cart.html', {'products': products, 'offers': offers, 'codes': codes})
    else:
        codes = ''
        codes = request.POST.get('getcode')
        offers = Offer.objects.all()
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        return render(request, 'cart.html', {'products': products, 'offers': offers, 'codes': codes})

METHOD_CHOICES = [
    ('mobile_money_Orange', 'Mobile Money - Orange'),
    ('mobile_money_Lonestar', 'Mobile Money - Lonestar'),
    ('bank_transfer', 'Bank Transfer - Daniel M.C. Padmore'),
]

def thank_you(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        # Redirect to login page or show appropriate message
        return redirect('login')  # Change 'login' to your actual login page URL or template

    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        carts = request.session.get('cart')
        products = Product.get_products_by_id(list(carts.keys()))

        # Validate phone number
        if len(phone) == 10 and phone.startswith("0778"):
            # Check if the form data is valid
            form = ElvisForm(request.POST, request.FILES)
            if form.is_valid():
                # Assign the user to the form instance before saving
                form.instance.user = request.user
                form.save()

                # Place orders
                for product in products:
                    order = Order.objects.create(
                        user=request.user,
                        product=product,
                        price=product.price,
                        quantity=carts.get(str(product.id)),
                        address=address,
                        phone=phone
                    )
                    order.place_order()

                # Clear the cart
                request.session['cart'] = {}

                return render(request, 'thank_you.html')
            else:
                # Form is invalid, display error messages
                messages.error(request, 'Invalid form data')
        else:
            messages.error(request, 'Invalid Phone number or phone number should have 10 digits')
    return redirect('cart')  # Redirect back to the cart page

def payment(request):
    if request.method == 'POST':
        payment_type = request.POST.get('payment_type')
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        screenshot = request.FILES.get('screenshot')

        # Create and save the Elvis object
        pay = Elvis(payment_type=payment_type, name=name, contact=contact, screenshot=screenshot)
        pay.save()

        # Redirect to the thank_you URL after successful payment
        return redirect('thank_you')

    
    
