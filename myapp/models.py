from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    code=models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    type = models.CharField(max_length=100,null = True)
    color=models.CharField(max_length=20)
    size=models.CharField(max_length=3)
    sex=models.CharField(max_length=10,null=True)
    price=models.IntegerField()
    stock = models.IntegerField()
    availability = models.BooleanField()
    date_added = models.DateField(auto_now_add=True)
    image = models.ImageField(null=False,blank=False)

    def __str__(self):
        return self.name


class Client (models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50,default = "070 000 000")
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    def __str__(self):
        return f"{self.firstName} {self.lastName}"

class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Shopping cart for user {self.user.username}"
    
class ProductInShoppingCart(models.Model):
    id = models.IntegerField(primary_key=True)
    shoppingCart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Item {self.product.name} x {self.quantity}"

class Card(models.Model):
    cardNumber = models.CharField(max_length=16)
    expirationDate = models.CharField(max_length=5)
    cvv = models.CharField(max_length=3)
    cardHolder = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.cardNumber

class Payment(models.Model):
    code = models.AutoField(primary_key=True)
    date = models.DateField(auto_now=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    shoppingCart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, blank=True, null=True)
    deliveryAddress = models.CharField(max_length=50)
    paymentAddress = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"payment {self.code}"
