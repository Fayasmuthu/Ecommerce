from django.urls import path
from . import views
from django.views.generic import TemplateView
from .views import CreateStripeCheckoutSessionView
from .views import SuccessView, CancelView


app_name = "order"

urlpatterns = [
    path("", views.index, name="index"),
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/<int:id>/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
    path('cart/checkout-detail/',views.checkout_detail,name='checkout_detail'),
    path('cart/checkout-shipping/',views.checkout_shipping,name='checkout_shipping'),
    path('cart/checkout-payment/',views.checkout_payment,name='checkout_payment'),
    path('cart/checkout-review/',views.checkout_review,name='checkout_review'),
    path('cart/checkout-complete/',views.checkout_complete,name='checkout_complete'),

    # My account 
    path('account/profile/',views.account_profile,name='account_profile'),
    path('account/order/',views.account_order,name='account_order'),
    path('add_to_wishlist/<int:store_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist_page, name='wishlist_page'), 

    # Stripe
     path(
        "create-checkout-session/<int:store_id>/",
        CreateStripeCheckoutSessionView.as_view(),
        name="create-checkout-session",
    ),
    path('success/', SuccessView.as_view(), name='success'),
    path('cancel/', CancelView.as_view(), name='cancel'),
]