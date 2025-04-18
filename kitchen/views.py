from django.shortcuts import render,redirect,get_object_or_404

from django.views.generic import View

from kitchen.models import User,Product,Cart,Order,OrderItem,Category,WishList,ReviewModel,DeliveryPerson,DeliveryAssignment

from django.db.models import Q,Sum

from kitchen.forms import SignupForm,SignInForm,CategoryForm,ProductForm,OrderForm,ReviewForm,DeliveryForm

from django.contrib.auth import authenticate,login,logout

from django.contrib import messages

from django.utils import timezone

from django.utils.decorators import method_decorator

from kitchen.decorators import signin_required

import razorpay
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
from django.urls import reverse





# signup view
RZP_KEY_ID='rzp_test_Sjy6Si9Hn24pDd'
RZP_KEY_SECRET='3nGtAZUZpwQz9DrxG4Q3WRYk'

class SignUpView(View):

    template_name='signup.html'

    form_class = SignupForm

    def get(self,request,*args,**kwargs):

        form_instance = self.form_class()

        return render(request,self.template_name,{'form':form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=self.form_class(request.POST)

        if form_instance.is_valid():

            form_instance.save()

            return redirect('login')
            
        return render(request,self.template_name,{'form':form_instance})
    
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

class SignInView(View):
    template_name = 'login.html'
    form_class = SignInForm

    @method_decorator(csrf_protect)
    def get(self, request, *args, **kwargs):
        form_instance = self.form_class()
        return render(request, self.template_name, {'form': form_instance})

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        form_instance = self.form_class(request.POST)
        if form_instance.is_valid():
            uname = form_instance.cleaned_data.get('username')
            pwd = form_instance.cleaned_data.get('password')
            user_object = authenticate(username=uname, password=pwd)
            
            if user_object:
                login(request, user_object)
                if user_object.is_staff:
                    return redirect('operations')
                
                elif user_object.role == "delivery_person":
                    return redirect('delivery-index')

                
                else:
                
                    return redirect('index')
                
        return render(request, self.template_name, {'form': form_instance})


class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect('login') 

@method_decorator(signin_required,name='dispatch')     

class AdminDashBoardView(View):

    template_name = 'admin_dashboard.html'   

    def get(self,request,*args,**kwargs):

        product_count = Product.objects.all().count()

        cat_count = Category.objects.all().count()

        today = timezone.now().date()

        
        today_order_count = Order.objects.filter(created_at__date=today).count()

        current_month = timezone.now().month
        current_year = timezone.now().year
        
        # Filter orders from the current month and year
        monthly_orders = Order.objects.filter(
            created_at__month=current_month,
            created_at__year=current_year
        )
        
        # Sum the total amount for orders in the current month
        monthly_revenue = OrderItem.objects.filter(
            order_object__in=monthly_orders
        ).aggregate(
            total_revenue=Sum('price')  # Sum the price of all items
        )['total_revenue'] or 0




        return render(request,self.template_name,{'product_count':product_count,'cat_count':cat_count,'today_order_count':today_order_count,'monthly_revenue':monthly_revenue})  
    
@method_decorator(signin_required,name='dispatch')
class AllOrdersView(View):

    template_name = 'all_order_details.html'

    def get(self, request, *args, **kwargs):
        # Retrieve all orders with related OrderItems and customer
        all_orders = Order.objects.prefetch_related('orderitems').order_by('-created_at')

        # Calculate the total amount for each order
        for order in all_orders:
            # Calculate total amount by summing item totals for the order
            order.total_amount = sum(item.item_total() for item in order.orderitems.all())

        # Prepare the context to pass to the template
        context = {
            'orders': all_orders
        }

        # Render the template
        return render(request, self.template_name, context)
    
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from .models import Order

class OrderStatusUpdateView(View):
    def post(self, request, order_id, *args, **kwargs):
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')

        if new_status in ['Pending', 'Confirmed', 'Out of Delivery', 'Delivered']:
            order.status = new_status
            order.save()
            messages.success(request, f"Order {order.id} status updated to {new_status}.")
        else:
            messages.error(request, "Invalid status selected.")

        return redirect('all-orders')
    
        




class IndexView(View):

    template_name='index.html'

    def get(self,request,*args,**kwargs):

        return render(request,self.template_name) 

@method_decorator(signin_required,name='dispatch')

class CategoryAddview(View):

    template_name = 'category.html' 

    form_class = CategoryForm

    def get(self,request,*args,**kwargs):

        form_instance = self.form_class()

        return render(request,self.template_name,{'form':form_instance})  

    def post(self,request,*args,**kwargs):

        form_instance = self.form_class(request.POST)   

        if form_instance.is_valid():

            form_instance.save()

            return redirect('add-category') 
        
        return render(request,self.template_name,{'form':form_instance})

@method_decorator(signin_required,name='dispatch')
   
class ProductAddView(View):

    template_name = 'product_add.html'

    form_class = ProductForm  

    def get(self,request,*args,**kwargs):

        form_instance = self.form_class()

        return render(request,self.template_name,{'form':form_instance})


    def post(self,request,*args,**kwargs):

        form_instance = self.form_class(request.POST,files=request.FILES)

        if form_instance.is_valid():

            form_instance.save()

            return redirect('add-product')

        return render(request,self.template_name,{'form':form_instance}) 
    
@method_decorator(signin_required,name='dispatch')

class ProductListView(View):

    template_name = 'product_list.html'

    def get(self, request, *args, **kwargs):

        search_text=request.GET.get('search-text')

        print('=========',search_text)

        if search_text:

            products = Product.objects.filter(Q(name__contains=search_text))

        else:   

            products = Product.objects.all()  # Fetch all products

        return render(request, self.template_name, {'products': products})
    
@method_decorator(signin_required,name='dispatch')    
class ProductUpdateView(View):

    template_name = 'product_update.html'

    form_class = ProductForm

    def get(self, request, pk, *args, **kwargs):

        product = get_object_or_404(Product, pk=pk)  # Get the product or show 404

        form_instance = self.form_class(instance=product)

        return render(request, self.template_name, {'form': form_instance, 'product': product})

    def post(self, request, pk, *args, **kwargs):

        product = get_object_or_404(Product, pk=pk)

        form_instance = self.form_class(request.POST, request.FILES, instance=product)

        if form_instance.is_valid():

            form_instance.save()

            return redirect('product-list')  # Redirect to product list after update

        return render(request, self.template_name, {'form': form_instance, 'product': product})
    
@method_decorator(signin_required,name='dispatch')
class ProductDeleteView(View):

    template_name = 'product_confirm_delete.html'

    def get(self, request, pk, *args, **kwargs):

        product = get_object_or_404(Product, pk=pk)

        return render(request, self.template_name, {'product': product})

    def post(self, request, pk, *args, **kwargs):

        product = get_object_or_404(Product, pk=pk)

        product.delete()
        
        return redirect('product-list')  # Redirect to product list after deletion
    
class ProductListUserView(View):
    
    template_name = 'product_userview.html'

    def get(self, request, *args, **kwargs):

        category = kwargs.get('category')  

        search_text = request.GET.get('search-text')

        products = Product.objects.all()


        print("========",search_text) 

        if search_text:

            products = products.filter(Q(name__icontains=search_text))  

            
       


        if category:

            # print("==========", category)  

            category_obj = get_object_or_404(Category,name = category)

            products = products.filter(category=category_obj)

         

        return render(request, self.template_name, {'products': products, 'selected_category': category})

    
    

class ProductDetailView(View):

    template_name = 'product_details.html' 

    def get(self, request, *args, **kwargs):

        id = kwargs.get('pk')

        
        product = get_object_or_404(Product, id=id)

        product_review = ReviewModel.objects.filter(product=product)

        return render(request, self.template_name, {'product': product,'reviews':product_review})
    
@method_decorator(signin_required,name='dispatch')

class AddToCartView(View):

    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:

            messages.error(request, "You must be logged in to add items to the cart.")

            return redirect('login') 

        product_id = kwargs.get('pk')

        product_instance = get_object_or_404(Product, id=product_id)       

        try:
            qty = request.POST.get('quantity') 
        except ValueError:
            messages.error(request, "Invalid quantity selected.")

            return redirect('product_detail', pk=product_id)

    
        Cart.objects.create(
            product_object=product_instance,
            quantity=qty,
            owner=request.user
        )

        messages.success(request, "Product added to cart successfully!")

        return redirect('index')

@method_decorator(signin_required,name='dispatch')
class CartSummaryView(View):

    template_name  ='cart_summary.html'

    def get(self,request,*args,**kwargs):

        qs = Cart.objects.filter(owner=request.user,is_order_placed = False)

        basket_total  = sum([c.item_total() for c in qs])

        return render(request,self.template_name,{'data':qs,'basket_total': basket_total}) 

    
@method_decorator(signin_required,name='dispatch')
class CartItemDeleteView(View):


    def get(self,request,*args,**kwargs):

        id = kwargs.get('pk')

        qs = Cart.objects.get(id=id).delete()

        return redirect('cart-summary')  
    
@method_decorator(signin_required,name='dispatch')
class PlaceOrderView(View):

    template_name = 'place_order.html'

    form_class = OrderForm

    def get(self,request,*args,**kwargs):

        form_instance = self.form_class()

        qs = Cart.objects.filter(owner=request.user,is_order_placed=False)

        basket_total = sum([c.item_total() for c in qs])

        return render(request,self.template_name,{'form':form_instance,'cartitems':qs,'total':basket_total})
    
    def post(self,request,*args,**kwargs):

        form_instance = self.form_class(request.POST)

        if form_instance.is_valid():

            form_instance.instance.customer = request.user   #here instance refer to the model given in model form

            form_instance.instance.location = request.POST.get('location')

            order_object = form_instance.save()

            cart_items = Cart.objects.filter(owner=request.user,is_order_placed = False)

            for ci in cart_items:

                OrderItem.objects.create(

                    order_object = order_object,
                    product_object = ci.product_object,
                    quantity = ci.quantity,
                    price = ci.product_object.price

                )

                ci.is_order_placed=True
                
                ci.save()


            payment_method = request.POST.get("payment_method") #ONLINE,COD

            if payment_method == 'ONLINE':

                client = razorpay.Client(auth=(RZP_KEY_ID,RZP_KEY_SECRET))

                data = { "amount": order_object.order_total()*100, "currency": "INR", "receipt": "order_rcptid_11" }

                payment = client.order.create(data=data)

                print("===============",payment)

                rzp_id = payment.get('id')

                order_object.rzp_order_id=rzp_id

                order_object.save()
                print(order_object.rzp_order_id)
                context = {
                    'key_id':RZP_KEY_ID,
                    'amount':order_object.order_total()*100,
                    'order_id':order_object.rzp_order_id

                }

                return render(request,'payment.html',context)

            return redirect('order-success')  
        
  
import json


class PaymentVerificationsView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        client = razorpay.Client(auth=(RZP_KEY_ID, RZP_KEY_SECRET))

        try:
            body = json.loads(request.body)
            rzp_order_id = body.get('razorpay_order_id')
            rzp_payment_id = body.get('razorpay_payment_id')
            rzp_signature = body.get('razorpay_signature')

            print("Received Razorpay Response:", body)

            # Verify the payment signature
            client.utility.verify_payment_signature({
                'razorpay_order_id': rzp_order_id,
                'razorpay_payment_id': rzp_payment_id,
                'razorpay_signature': rzp_signature
            })

            # Update order status
            Order.objects.filter(rzp_order_id=rzp_order_id).update(is_paid=True)
            Order.objects.filter(rzp_order_id=rzp_order_id).update(status='Confirmed')


            # Send JSON response with redirect URL
            return JsonResponse({"status": "success", "redirect_url": reverse('order-success')})

        except Exception as e:
            print('Payment Failed:', str(e))
            return JsonResponse({"status": "error", "message": "Payment verification failed"})


       

class OrderSuccessMessage(View):

    template_name ='order_success_msg.html'   

    def get(self,request,*args,**kwargs):


        return render(request,self.template_name) 

@method_decorator(signin_required,name='dispatch')
class OrderSummaryView(View):

    template_name = "order_summary.html"

    def get(self,request,*args,**kwargs):

        qs = Order.objects.filter(customer = request.user).order_by("-created_at")

        return render(request,self.template_name,{'orders':qs})  


@method_decorator(signin_required,name='dispatch')
class AddWishlistView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to add items to the wishlist.")
            return JsonResponse({"error": "Authentication required"}, status=401)

        product_id = kwargs.get('pk')
        product_instance = get_object_or_404(Product, id=product_id)
        
        wishlist, created = WishList.objects.get_or_create(user=request.user)

        if product_instance in wishlist.product.all():
            wishlist.product.remove(product_instance)
            wishlist.refresh_from_db()
            return JsonResponse({"removed": True})  
        else:
            wishlist.product.add(product_instance)
            wishlist.refresh_from_db()
            return JsonResponse({"added": True})  


@method_decorator(signin_required,name='dispatch')
class WishlistView(View):
    template_name = 'wishlist.html'

    def get(self,request,*args,**kwargs):
    
        wishlist, created = WishList.objects.get_or_create(user=request.user)
        
        products = wishlist.product.all()  # Get all wishlist items

        return render(request,self.template_name, {"wishlist_products": products})
    



class RemoveFromWishlistView(View):
    def post(self, request, *args, **kwargs):
        product_id = kwargs.get("pk")
        product = get_object_or_404(Product, id=product_id)

        # Remove the product from the wishlist
        wishlist_item = WishList.objects.filter(user=request.user, product=product)
        if wishlist_item.exists():
            wishlist_item.delete()

            # Get updated wishlist count
            wishlist_count = WishList.objects.filter(user=request.user).count()
            return JsonResponse({"removed": True, "wishlist_count": wishlist_count})

        return JsonResponse({"removed": False, "wishlist_count": WishList.objects.filter(user=request.user).count()})
    

@method_decorator(signin_required,name='dispatch')
class AddReviewView(View):

    template_name = 'add_review.html'

    form_class =  ReviewForm

    def get(self,request,*args,**kwargs):

        id = kwargs.get('pk')

        qs = Product.objects.get(id=id)

        form_instance = self.form_class() 

        return render(request,self.template_name,{'form':form_instance,'product':qs}) 

    def post(self,request,*args,**kwargs):

        id = kwargs.get('pk') 

        product = Product.objects.get(id=id)

        form_instance = self.form_class(request.POST)

        if form_instance.is_valid():

            review = form_instance.save(commit=False)

            review.user = request.user

            review.product = product

            review.verified_purchase = True  
            
            review.save()

            messages.success(request, "Your review has been submitted!")

            return redirect('product-details', pk=product.id)
        
        return render(request,self.template_name,{'form':form_instance})
    

    #  DELIVERY PERSON 


class DeliveryPersonIndexView(View):

    template_name = 'delivery_index.html'

    def get(self,request,*args,**kwargs):


        return render(request,self.template_name)
    

class DeliveryProfileCreateView(View):

    template_name='profile.html'

    form_class = DeliveryForm 

    def get(self,request,*args,**kwargs):

        form_instance = self.form_class()

        return render(request,self.template_name,{'form':form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=self.form_class(request.POST)

        if form_instance.is_valid():
            delivery_person = form_instance.save(commit=False)  # Create instance but don't save yet
            delivery_person.user = request.user  # Assign the logged-in user
            delivery_person.save()  # Now save the instance

            return redirect('delivery-index')

        return render(request, self.template_name, {'form': form_instance})
    
class DeliveryProfileUpdateView(View):


    template_name='profile_update.html'

    form_class = DeliveryForm 

    def get(self,request,*args,**kwargs):

        id = kwargs.get('pk')

        qs = DeliveryPerson.objects.get(user_id=id)

        form_instance = self.form_class(instance=qs)

        return render(request,self.template_name,{'form':form_instance})
    
    def post(self,request,*args,**kwargs):
        id = kwargs.get('pk')

        qs = DeliveryPerson.objects.get(user_id=id)

        form_instance=self.form_class(request.POST,instance=qs)

        if form_instance.is_valid():
            delivery_person = form_instance.save(commit=False)  # Create instance but don't save yet
            delivery_person.user = request.user  # Assign the logged-in user
            delivery_person.save()  # Now save the instance

            return redirect('delivery-index')

        return render(request, self.template_name, {'form': form_instance})
    

from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Order, DeliveryPerson

class DeliveryOrderListView(View):
    template_name = 'delivery_details.html'

    def get(self, request, *args, **kwargs):
        # Ensure the user is a delivery person
        if not hasattr(request.user, 'delivery_profile'):
            return render(request, self.template_name, {'orders': []})

        delivery_person = request.user.delivery_profile  

        # Fetch orders where status is 'Out of Delivery' and location matches
        orders = Order.objects.filter(status="Out of Delivery", location=delivery_person.location)

        # print(orders)

        return render(request, self.template_name, {'orders': orders})
    



from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.urls import reverse
from .models import Order, DeliveryAssignment

@login_required
def update_order_status(request, order_id):
    """Update the order status to 'Delivered' and assign the delivery person."""
    
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        person_id = request.POST.get("delivery_person")

        if not person_id:
            return HttpResponseForbidden("❌ Delivery person ID is missing.")

        try:
            delivery_person = User.objects.get(id=person_id)
            order.delivery_person = delivery_person  # Assign the delivery person
            order.status = "Delivered"
            order.save()
            print(f"✅ Delivery person assigned: {delivery_person.username}")
        except User.DoesNotExist:
            print("❌ Error: Delivery person not found!")
            return HttpResponseForbidden("Delivery person does not exist.")

        return redirect(reverse("delivery_orders"))  # ✅ Ensure this URL name is correct

    return redirect(reverse("delivery_orders"))  # In case of GET request, redirect back



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Order

@login_required
def delivery_history(request):
    """Get all delivered orders assigned to the logged-in delivery person."""
    
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in to view this page.")

    # Get orders delivered by the logged-in delivery person
    delivered_orders = Order.objects.filter(
        delivery_person=request.user,
        status="Delivered"
    ).order_by("-updated_at")  # Show latest first

    context = {
        "delivered_orders": delivered_orders
    }
    return render(request, "delivery_history.html", context)










