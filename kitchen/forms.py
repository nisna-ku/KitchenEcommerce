from django import forms

from django.contrib.auth.forms import UserCreationForm

from kitchen.models import User,Category,Product,Order,OrderItem,ReviewModel,DeliveryPerson


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

#product add form 

class ProductForm(forms.ModelForm):

    class Meta:

        model = Product

        fields = ["name","description","price","stock","category","image"] 

#order form

class OrderForm(forms.ModelForm):

    class Meta:

        model = Order 

        fields = ["address","phone","payment_method","location"]

#review form

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewModel

        fields = ['rating', 'review_text', 'images']
        
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)], attrs={'class': 'form-control'}),
            'review_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'images': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }    

class DeliveryForm(forms.ModelForm):

    class Meta:
        model = DeliveryPerson
        fields = ['phone_number_1','phone_number_2','address','location']

   