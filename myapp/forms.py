from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1})
    )

class PaymentForm(forms.Form):
    firstName = forms.CharField(label='First Name', max_length=50)
    lastName = forms.CharField(label='Last Name', max_length=50)
    email = forms.CharField(label='Email')
    phone = forms.CharField(label='Phone', max_length=9,help_text='Format: 07*******')
    cardNumber = forms.CharField(label='Card Number', max_length=16)
    cardHolder = forms.CharField(label='Cardholder Name', max_length=100)
    expirationDate = forms.CharField(label='Expiration Date', max_length=5, help_text='Format: MM/YY')
    cvv = forms.CharField(label='CVV', max_length=3)
    deliveryAddress = forms.CharField(label='Delivery Address', widget=forms.Textarea)
    paymentAddress = forms.CharField(label='Payment Address', widget=forms.Textarea)
    city = forms.CharField(label='City', max_length=100)
    country = forms.CharField(label='Country', max_length=100)
    comment = forms.CharField(label='Comment', widget=forms.Textarea, required=False)
