from django.db import models

from django.contrib.auth.models import AbstractUser

# user model

class User(AbstractUser):

    ADMIN = 'admin'
    DELIVERY_PERSON = 'delivery_person'
    CUSTOMER = 'customer'
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (DELIVERY_PERSON, 'Delivery Person'),
        (CUSTOMER, 'Customer'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES,default=CUSTOMER)

    is_staff = models.BooleanField(default=False)

    phone = models.CharField(max_length=15, blank=True, null=True)


# Category Model
class Category(models.Model):

    CATEGORY_OPTIONS = [
    ('appliances', 'Kitchen Appliances'),
    ('Cookware', 'Cookware'),
    ('utensils', 'Utensils'),
    ('storage', 'Storage & Containers'),
    ('cleaning', 'Cleaning Supplies'),
]

    name = models.CharField(max_length=255,choices=CATEGORY_OPTIONS,default='Cookware')

    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

# Product Model

class Product(models.Model):

    name = models.CharField(max_length=255)

    description = models.TextField()

    price = models.DecimalField(max_digits=10, decimal_places=2)

    stock = models.PositiveIntegerField()

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    image = models.ImageField(upload_to='product_images/', blank=True, null=True)

    rating = models.FloatField(default=0.0,null=True)
    
    def __str__(self):
        
        return self.name

class Cart(models.Model):

    product_object=models.ForeignKey(Product,on_delete=models.CASCADE)

    owner=models.ForeignKey(User,on_delete=models.CASCADE)

    quantity=models.PositiveIntegerField()

    is_order_placed=models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now_add=True)


    def item_total(self):

        return self.quantity*self.product_object.price


class Order(models.Model):

    customer=models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")

    address=models.TextField(null=False, blank=False)

    phone=models.CharField(max_length=20, null=False, blank=False)
    
    PAYMENT_OPTIONS=(
        ("COD","COD"),
        ("ONLINE","ONLINE")
    )

    payment_method=models.CharField(max_length=15, choices=PAYMENT_OPTIONS, default="COD")

    rzp_order_id=models.CharField(max_length=100, null=True)

    is_paid=models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now_add=True)

    def order_total(self):

        total = 0

        order_items=self.orderitems.all()

        if order_items:

            total = sum([oi.item_total() for oi in order_items])

        return total    
    


class OrderItem(models.Model):

    order_object=models.ForeignKey(Order,on_delete=models.CASCADE, related_name="orderitems")

    product_object=models.ForeignKey(Product, on_delete=models.CASCADE)
    
    quantity=models.PositiveIntegerField(default=1)
    
    price=models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now_add=True)

    def item_total(self):
        
        return self.price*self.quantity  

class WishList(models.Model):

    product = models.ManyToManyField(Product) 

    user = models.OneToOneField(User,on_delete=models.CASCADE) 

    def __str__(self):
        return self.product       




   
