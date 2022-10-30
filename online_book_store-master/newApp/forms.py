from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class SignupForm(forms.Form):
    user_id = forms.CharField(max_length = 30)
    email = forms.EmailField(max_length=200, help_text='required')
    password = forms.CharField(max_length = 30)
    first_name = forms.CharField(max_length = 30)
    middle_name = forms.CharField(max_length = 30)
    last_name = forms.CharField(max_length = 30)
    phone_no = forms.CharField(max_length = 30 )

    class Meta:
        model = Customer
        fields = ('user_id', 'email', 'password', 'first_name','middle_name','last_name', 'phone_no')

class LoginForm(forms.Form):
    user_id = forms.CharField(max_length = 30)
    password = forms.CharField(max_length = 30)

class StoreSignUp(forms.ModelForm):
    class Meta:
        model = Book_store
        fields = ['store_name', 'email', 'password', 'website','phone_no', 'rating', 'address_line1', 'address_line2',
        'city', 'district', 'state', 'zip_code']

class storeLoginForm(forms.Form):
    email = forms.CharField(max_length = 50)
    password = forms.CharField(max_length = 50)

class bookAddForm(forms.Form):
    title = forms.CharField(max_length = 50)
    author = forms.CharField(max_length = 50)
    publisher = forms.CharField(max_length = 50)
    genre = forms.CharField(max_length = 20)
    year_of_publish = forms.IntegerField(min_value=1750)
    price = forms.IntegerField()
    no_of_books = forms.IntegerField()

class userAddressForm(forms.ModelForm):
    
    class Meta:
        model = Customer_address
        fields = ['address_line1', 'address_line2', 'city', 'district', 'state', 'zip_code']

