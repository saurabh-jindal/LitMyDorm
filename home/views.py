from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Category, Product, Images, OrderItem, Order, Address, Contact, Slide
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Create your views here

"""
    Basic API
"""
def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    slides = Slide.objects.all()
    context = {
        'categories': categories,
        'products' : products,
        'slides' : slides
    }

    return render(request, 'home/index.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        contact = Contact(
            name=  name,
            email = email,
            subject = subject,
            message = message
        )
        contact.save()
        messages.success(request, "Your message has been recieved")
    return render(request, 'home/contact.html')

def category(request, slug):
    category = Category.objects.filter(slug=slug).first()
    products = Product.objects.filter(category=category)
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'home/category.html', context)


def view_product(request, slug):
    product = Product.objects.filter(slug=slug).first()
    context = {
        'product': product,
    }
    return render(request, 'home/product.html', context)


"""
    Cart API or logic
"""


@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        product=product,
        is_ordered=False,
        user=request.user
    )
    order_query = Order.objects.filter(user=request.user, is_ordered=False)
    if order_query.exists():
        order = order_query[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Item quantity is updated!")
            return redirect('order_summary')
        else:
            order.products.add(order_item)
            messages.success(request, "Item is successfully added to cart!")
            return redirect('order_summary')
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user,
            ordered_date=ordered_date
        )
        order.products.add(order_item)
        messages.success(request, "Item is successfully added to the Cart!")
        return redirect('order_summary')


@login_required()
def order_summary(request):
    try:
        order = Order.objects.get(user=request.user, is_ordered=False)
        context = {
            'object': order
        }
        return render(request, 'home/cart.html', context)
    except ObjectDoesNotExist:
        messages.error(request, "You do not have any active order")
        return redirect('index')


@login_required
def checkout(request):
    if request.method == 'GET':
        try:
            order = Order.objects.get(user=request.user, is_ordered=False)
            context = {
                'order': order,
            }
            return render(request, 'home/checkout.html', context)
        except ObjectDoesNotExist:
            messages.info(request, "You do not have any active order")
            return redirect('home:checkout')

    if request.method == 'POST':
        order = Order.objects.get(user=request.user, is_ordered=False)
        apartment_address = request.POST['apartment_address']
        street_address = request.POST['street_address']
        country = request.POST['country']
        zip = request.POST['zip']
        phone = request.POST['phone']
        payment_option = request.POST['payment_option']
        print(payment_option)

        address = Address(
            user=request.user,
            apartment_address=apartment_address,
            street_address=street_address,
            country=country,
            zip=zip,
            phone=phone
        )
        address.default = True
        address.save()
        order.address = address
        order.save()

        if payment_option == 'card':
            return redirect('payment', payment_option='card')
        elif payment_option == 'paytm':
            return redirect('payment', payment_option='paytm')
        elif payment_option == 'delivery':
            return redirect('payment', payment_option='delivery')
        else:
            messages.error(request, "Invalid Payment Option")
            return redirect(order_summary)

@login_required
def payment(request, payment_option):
    if payment_option == 'delivery':
        return HttpResponse("You have choosen for Pay on delivery. Our agent will communicate with you in short time")
    elif payment_option == 'paytm':
        return HttpResponse("You are eligible for some gifts item")
    elif payment_option == 'card':
        return HttpResponse("We Congratulate you for your order")
    else:
        return HttpResponse("Go fuck yourself! You cannot hack me.")




"""
Auth API
"""


def handleSignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # check for error
        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = first_name
        myuser.last_name = last_name
        myuser.save()
        messages.success(request, 'you have been successfully signed up!')
        return redirect('/')

    else:
        return redirect('index')


def handleLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, "invalid parameters")
            return redirect('/')
        else:
            login(request, user)
            messages.success(request, "You have been successfully logged in!")
            return redirect('/')
    else:
        messages.error(request, "You should Log in first!")
        return redirect('index')


def handleLogout(request):
    logout(request)
    messages.success(request, "You have been successfully Logout!")
    return redirect('index')
