"""
URL configuration for kitchenAppliances project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from kitchen import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.SignUpView.as_view(),name='register'),
    path('signin/',views.SignInView.as_view(),name='login'),
    path('signout/',views.SignOutView.as_view(),name='logout'),
    path('index/',views.IndexView.as_view(),name='index'),
    path('add/category/',views.CategoryAddview.as_view(),name='add-category'),
    path('add/product/',views.ProductAddView.as_view(),name='add-product'),
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('product/update/<int:pk>/',views.ProductUpdateView.as_view(), name='update-product'),
    path('product/delete/<int:pk>/',views.ProductDeleteView.as_view(), name='delete-product'),
    path('product/userview/',views.ProductListUserView.as_view(),name='user-product-view'),
    path('products/category/<str:category>/',views.ProductListUserView.as_view(), name='product-category'),
    path('product/<int:pk>/details/',views.ProductDetailView.as_view(),name='product-details'),
    path('addtocart/<int:pk>/',views.AddToCartView.as_view(),name="add-to-cart"),
    path('cart/summary/',views.CartSummaryView.as_view(),name='cart-summary'),
    path('cart/<int:pk>/remove/',views.CartItemDeleteView.as_view(),name='cart-item-remove'),
    path('place/order/',views.PlaceOrderView.as_view(),name='place-order'),
    path('success/msg/',views.OrderSuccessMessage.as_view(),name='order-success'),
    path('order/summary/',views.OrderSummaryView.as_view(),name='order-summary'),
    path('payment/verify/',views.PaymentVerificationsView.as_view(), name='payment-verification'),
    path('operations/',views.AdminDashBoardView.as_view(),name='operations'),
    path('all/orders/',views.AllOrdersView.as_view(),name='all-orders'),
    path('wishlist/add/<int:pk>/',views.AddWishlistView.as_view(),name='add_to_wishlist'),
    path("wishlist/", views.WishlistView.as_view(), name="wishlist"),
    path('wishlist/remove/<int:pk>/', views.RemoveFromWishlistView.as_view(), name='remove_from_wishlist'),
    path('product/<int:pk>/add-review/',views.AddReviewView.as_view(), name='add_review'),







]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
