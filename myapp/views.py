from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from myapp.forms import AddToCartForm, CreateUserForm, PaymentForm
from myapp.models import *
# Create your views here.
def home(request):
    return render(request, 'home.html')
def shop(request):
    return render(request,'shop.html')
def shop_men(request):
    return render(request,'shop_men.html')
def shop_women(request):
    return render(request,'shop_women.html')
def random(request):
    data = Product.objects.all()
    context = {'inventory': data}
    return render(request, 'random.html', context)
def products(request, type_name,sex_name):
    data = Product.objects.filter(type=type_name,sex=sex_name)
    context = {'items': data, 'type': type_name,'sex':sex_name}
    return render(request, 'products.html', context)
def profile(request):
    return render(request, "profile.html")

def payment(request):
    return render(request, "payment.html")

def singleProduct(request, code):
    product = get_object_or_404(Product, code=code)
    context={'id' : id,'product' : product}
    return render(request, 'singleProduct.html', context)

def successfulPayment(request):
    return render(request, "successfulPayment.html")


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('/')
    else :
        form = CreateUserForm()

        if request.method =='POST':
            form=CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
        context = {'form' : form}
        return render(request,'register.html',context)
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('/')
    else :
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password = password)

            if user is not None:
                login(request,user)
                return redirect('/')
            else:
                error = 'Invalid username or password'
        else : 
            error=None

        return render(request,'login.html',{'error': error})

def logoutUser(request):
    logout(request)
    return redirect('login')
@login_required(login_url='login')
def add_to_cart(request, product_code):
    product = get_object_or_404(Product, code=product_code)

    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            shoppingCart, created = ShoppingCart.objects.get_or_create(user=request.user)
            product, created = ProductInShoppingCart.objects.get_or_create(shoppingCart=shoppingCart, product=product, defaults={'quantity': quantity})
            if not created:
                product.quantity += quantity
                product.save()
            return redirect('shoppingCart')
    else:
        form = AddToCartForm()

    context = {
        'product': product,
        'form': form,
    }
    return render(request, 'shoppingCart.html', context)

def shoppingCart(request):
    if request.user.is_authenticated:
        shopping_cart_items = ProductInShoppingCart.objects.filter(shoppingCart__user=request.user)
        total_price = sum(item.quantity * item.product.price for item in shopping_cart_items)

        context = {
            'shopping_cart_items': shopping_cart_items,
            'total': total_price
        }
        return render(request, 'shoppingCart.html', context)
    else:
        return render(request, 'shoppingCart.html')
def remove_from_cart(request, item_id):
    if request.user.is_authenticated:
        try:
            item = ProductInShoppingCart.objects.get(pk=item_id)
            if item.shoppingCart.user == request.user:
                if request.method == 'POST':
                    quantity_to_remove = int(request.POST.get('quantity', 1))
                    if 1 <= quantity_to_remove <= item.quantity:
                        if quantity_to_remove == item.quantity:
                            item.delete()
                        else:
                            item.quantity -= quantity_to_remove
                            item.save()
        except ProductInShoppingCart.DoesNotExist:
            pass
    return redirect('shoppingCart')

def checkout(request):
    user = request.user

    shopping_cart_items = ProductInShoppingCart.objects.filter(shoppingCart__user=user)
    total_price = sum(item.quantity * item.product.price for item in shopping_cart_items)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            card_data = {
                'cardNumber': form.cleaned_data['cardNumber'],
                'expirationDate': form.cleaned_data['expirationDate'],
                'cvv': form.cleaned_data['cvv'],
                'cardHolder': request.user
            }

            # Check if a card with the same information exists
            existing_card = Card.objects.filter(
                cardNumber=card_data['cardNumber'],
                expirationDate=card_data['expirationDate'],
                cvv=card_data['cvv'],
                cardHolder=card_data['cardHolder']
            ).first()

            if existing_card:
                card = existing_card
            else:
                card = Card(**card_data)
                card.save()

            client_data = {
                'firstName': form.cleaned_data['firstName'],
                'lastName': form.cleaned_data['lastName'],
                'address': form.cleaned_data['deliveryAddress'],
                'email': form.cleaned_data['email'],
                'phone': form.cleaned_data['phone'],
                'user': request.user,
            }

            # Check if a client with the same information exists
            existing_client = Client.objects.filter(
                firstName=client_data['firstName'],
                lastName=client_data['lastName'],
                address=client_data['address'],
                email=client_data['email'],
                phone=client_data['phone'],
                user=client_data['user']
            ).first()

            if existing_client:
                client = existing_client
            else:
                client = Client(**client_data)
                client.save()

            payment_data = {
                'client': client,
                'deliveryAddress': form.cleaned_data['deliveryAddress'],
                'paymentAddress': form.cleaned_data['paymentAddress'],
                'city': form.cleaned_data['city'],
                'country': form.cleaned_data['country'],
                'card': card,
                'comment': form.cleaned_data['comment']
            }
            payment = Payment(**payment_data)
            payment.save()

            shopping_cart_items = ProductInShoppingCart.objects.filter(shoppingCart__user=user)
            shopping_cart_items.delete()

            return redirect('success')
    else:
        form = PaymentForm()

    context = {
        'form': form,
        'shopping_cart_items': shopping_cart_items,
        'total' : total_price,
    }
    return render(request, 'payment.html', context)
