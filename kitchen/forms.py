from django import forms

from django.contrib.auth.forms import UserCreationForm

from kitchen.models import User,Category,Product,Order,OrderItem


# signup form

class SignupForm(UserCreationForm):

    class Meta:

        model= User

        fields =["username","email","phone"]

#login form 

class SignInForm(forms.Form):

    username = forms.CharField(max_length=20)

    password = forms.CharField(max_length=20)  

# category add form

class CategoryForm(forms.ModelForm):

    class Meta:

        model = Category

        fields = ["name","description"]  

class ProductForm(forms.ModelForm):

    class Meta:

        model = Product

        fields = ["name","description","price","stock","category","image"]   

class OrderForm(forms.ModelForm):

    class Meta:

        model = Order 

        fields = ["address","phone","payment_method"]               