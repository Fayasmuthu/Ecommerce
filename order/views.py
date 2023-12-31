
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from products.models import Store
from django.contrib.auth.models import User
from . models import Orders,OrderItem,UserProfile,WishlistItem
from .forms import UserProfileForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.views import View
import stripe
from django.urls import reverse
from django.conf import settings
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.contrib import messages
from products.templatetags.course_tags import discount_calculation


# Create your views here.
def index(request):
    return render(request, "index.html")

@login_required
def account_profile(request):
    wishlist_count =request.user.wishlist.count()
    cart_items = request.session.get('cart', {})
    cart_total_amount = sum(item['price'] * item['quantity'] for item in cart_items.values())
    print("Cart Total Amount:", cart_total_amount)  # Add this line for debugging
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            user_profile = form.save(commit=False)
            if profile is None:
                user_profile.user = request.user
            user_profile.save()
            return redirect('order:account_profile')  # Redirect after successful update
    else:
        form = UserProfileForm(instance=profile)

    context={
        'form': form,
        'profile':profile,
        'wishlist_count': wishlist_count,
        'cart_items': cart_items,
        'cart_total_amount': cart_total_amount,
    }
    return render(request, 'account/account-profile.html', context)


@login_required
def account_order(request):
    user = request.user  # Get the current logged-in user
    orders = Orders.objects.filter(user=user)
    order_items = OrderItem.objects.filter(orders__in=orders)
    order_count = orders.count()
    wishlist_count =request.user.wishlist.count()
    profile = UserProfile.objects.get(user=request.user)
    cart_items = request.session.get('cart', {})
    cart_total_amount = sum(item['price'] * item['quantity'] for item in cart_items.values())
    print("Cart Total Amount:", cart_total_amount)  # Add this line for debugging



    #__________________-PAGINATION-_______________________
    paginator = Paginator(order_items, 8)

    page_number = request.GET.get('page')
    try:
        paginated_order_items = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_order_items = paginator.page(1)  
    except EmptyPage:
        paginated_order_items = paginator.page(paginator.num_pages)  

    #__________________-END PAGINATION-_____________________________

    context = {
        'order_items': order_items,
        'order_items': paginated_order_items,
        'order_count': order_count,
        'profile':profile,
        'wishlist_count': wishlist_count,
        'cart_items': cart_items,
        'cart_total_amount': cart_total_amount,

    }
    return render(request, "account/account-orders.html",context)


@login_required
def add_to_wishlist(request, store_id):
    store = get_object_or_404(Store, id=store_id)

    # store = Store.objects.get(id=store_id)
    wished = False
    if request.user in store.wishlisted_by.all():
        store.wishlisted_by.remove(request.user)
    else:
        store.wishlisted_by.add(request.user)
        wished = True
    wishlist_count = request.user.wishlist.count()
    success_message = f"{store.name} added to the wishlist successfully!"
    if wished:
        response_data = {
                    'wished': wished,
                    'wishlist_count': wishlist_count,
                    'message': success_message,
                }
    # return redirect('order:wishlist_page')
        return JsonResponse(response_data)
    else:
        return JsonResponse({'message': 'Remove from Wishlist'})
    


@login_required
def wishlist_page(request):
    wishlist_items =request.user.wishlist.all()
    wishlist_count =request.user.wishlist.count()
    profile = UserProfile.objects.get(user=request.user)
    cart_items = request.session.get('cart', {})
    cart_total_amount = sum(item['price'] * item['quantity'] for item in cart_items.values())

    context = {
        'wishlist_items': wishlist_items,
        'wishlist_count': wishlist_count,
        'cart_total_amount': cart_total_amount,
        'cart_items': cart_items,
        'profile':profile
    }
    return render(request, 'account/wishlist.html',context)


@login_required
def cart_add(request, id):
    # if not request.user.is_authenticated:
    #     return JsonResponse({'message': 'User not authenticated'}, status=401)
    cart = Cart(request)
    product = Store.objects.get(id=id)
    cart.add(product=product)
    
    cart_items = request.session.get('cart', {})
    cart_total_amount = sum(item['price'] * item['quantity'] for item in cart_items.values())

    # Customize the success message
    success_message = f"{product.name} added to the cart successfully!"
    
    response_data = {
        'cart_total_amount': cart_total_amount,
        'cart_count': len(cart_items),
        'message': success_message,
    }
    return JsonResponse(response_data)



@login_required
def item_clear(request, id):
    cart = Cart(request)
    product = Store.objects.get(id=id)
    cart.remove(product)
    # return redirect("order:cart_detail")
    cart_items = request.session.get('cart', {})
    cart_total_amount = sum(item['price'] * item['quantity'] for item in cart_items.values())
    
    response_data = {
        'cart_total_amount': cart_total_amount,
        'cart_count': len(cart_items),
    }
    return JsonResponse(response_data)


@login_required
def item_increment(request, id):
    cart = Cart(request)
    product = Store.objects.get(id=id)
    cart.add(product=product)
    
    cart_items = request.session.get('cart', {})
    cart_total_amount = sum(item['price'] * item['quantity'] for item in cart_items.values())
    item_total = discount_calculation(product.get_original_price(),product.get_price()) * cart.get_quantity(product)

    print('cart_count', len(cart_items))
    print('quantity',cart.get_quantity(product))
    print('cart_total_amount',cart_total_amount)
    print('item_total', item_total)

    
    response_data = {
        'cart_total_amount': cart_total_amount,
        'cart_count': len(cart_items),
        'quantity': cart.get_quantity(product),
        'item_total': item_total,
    }
    return JsonResponse(response_data)


@login_required
def item_decrement(request, id):
    cart = Cart(request)
    product = Store.objects.get(id=id)
    cart.decrement(product=product)
    
    item_total = discount_calculation(product.get_original_price(),product.get_price()) * cart.get_quantity(product)
    # Fetch updated cart data
    cart_items = request.session.get('cart', {})
    cart_total_amount = sum(item['price'] * item['quantity'] for item in cart_items.values())

    print('cart_count', len(cart_items))
    print('quantity',cart.get_quantity(product))
    print('cart_total_amount',cart_total_amount)
    print('item_total', item_total)

 

    # Prepare response data
    response_data = {
        'cart_total_amount': cart_total_amount,
        'cart_count': len(cart_items),
        'quantity': cart.get_quantity(product),  # Get updated quantity for the product
        'item_total': item_total,

    }
    return JsonResponse(response_data)


@login_required
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("order:cart_detail")


@login_required
def cart_detail(request):
    profile = UserProfile.objects.get(user=request.user)
    cart_items = request.session.get('cart', {})
    wishlist_count =request.user.wishlist.count()
    
    # Calculate total cart amount
    cart_total_amount = sum(item['price'] * item['quantity'] for item in cart_items.values())

    context = {
        'cart_items': cart_items,
        'cart_total_amount': cart_total_amount,
        'wishlist_count': wishlist_count,
        'cart_total_amount': cart_total_amount,
        'profile':profile
    }
    return render(request, 'cart/cart.html',context)


@login_required
def checkout_detail(request):
    profile = UserProfile.objects.get(user=request.user)
    cart_items = request.session.get('cart', {})
    wishlist_count =request.user.wishlist.count()

    cart_total_amount = sum(item['price'] * item['quantity'] for item in cart_items.values())
    print("Cart Total Amount:", cart_total_amount) 

    context = {
        'cart_items': cart_items,
        'cart_total_amount': cart_total_amount,
        'cart_total_amount': cart_total_amount,
        'cart_items': cart_items,
        'wishlist_count': wishlist_count,
        'profile':profile
    }
    return render(request, 'cart/checkout-details.html',context)


@login_required
def checkout_shipping(request):
    profile = UserProfile.objects.get(user=request.user)
    wishlist_count =request.user.wishlist.count()
    cart_items = request.session.get('cart', {})
    cart_total_amount = sum(item['price'] * item['quantity'] for item in cart_items.values())
    context={
        'cart_total_amount': cart_total_amount,
        'cart_items': cart_items,
        'profile':profile,
        'wishlist_count': wishlist_count,

        }
           

    if request.method == "POST":
        # Fetch user and cart information
        user_id = request.session.get('_auth_user_id')
        user = User.objects.get(id=user_id)
        cart = request.session.get('cart', {})

        # Retrieve shipping information from the form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone_number')
        company = request.POST.get('company')
        country = request.POST.get('country')
        state = request.POST.get('state')
        pincode = request.POST.get('pin_code')
        address = request.POST.get('address')
        address2 = request.POST.get('address2')

        order = Orders(
            user=user,
            first_Name=first_name,
            last_Name=last_name,
            email=email,
            phone=phone,
            company=company,
            country=country,
            state=state,
            postcode=pincode,
            address=address,
            address1=address2,
        )
        order.save()

        # Save order items related to this order
        for item_id, item_details in cart.items():
            a=float(item_details['price'])
            b=int(item_details['quantity'])
            total = a * b

            order_item = OrderItem(
                orders=order,
                store=item_details['name'],  # Replace with the correct field name
                image=item_details['image'],
                price=item_details['price'],
                quantity=item_details['quantity'],
                total=total,
                date_purchased=order.date_purchased 
            )
            order_item.save()

        # Clear the cart after the order is placed
        request.session['cart'] = {}
        # order_id = order.id
        # # Redirect to checkout payment page or any other relevant page
        # return redirect(reverse('order:create-checkout-session'}))
       
    return render(request, 'cart/checkout-shipping.html',context)


def checkout_payment(request):
    profile = UserProfile.objects.get(user=request.user)
    wishlist_count =request.user.wishlist.count()
    cart_items = request.session.get('cart', {})
    
    # Calculate total cart amount
    cart_total_amount = sum(item['price'] * item['quantity'] for item in cart_items.values())
    
    print("Cart Total Amount:", cart_total_amount)  # Add this line for debugging
    pk = 123
    print("PK Value:", pk)
    context = {
        'cart_items': cart_items,
        'cart_total_amount': cart_total_amount,
        'profile':profile,
        'wishlist_count': wishlist_count,
        'pk': pk 
    }
    return render(request, 'cart/checkout-payment.html',context)


def checkout_review(request):
    profile = UserProfile.objects.get(user=request.user)
    wishlist_count =request.user.wishlist.count()
    cart_items = request.session.get('cart', {})
    
    # Calculate total cart amount
    cart_total_amount = sum(item['price'] * item['quantity'] for item in cart_items.values())
    
    print("Cart Total Amount:", cart_total_amount)  # Add this line for debugging

    context = {
        'cart_items': cart_items,
        'cart_total_amount': cart_total_amount,
        'cart_total_amount': cart_total_amount,
        'cart_items': cart_items,
        'wishlist_count': wishlist_count,
        'profile':profile

    }
    return render(request, 'cart/checkout-review.html',context)


def checkout_complete(request):
    return render(request, 'cart/checkout-complete.html')




stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateStripeCheckoutSessionView(View):
    """
    Create a checkout session and redirect the user to Stripe's checkout page
    """

    def post(self, request, *args, **kwargs):
        price1 = Store.objects.all()
        
        for store in price1:
            price2=store.price
            name=store.name
        

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "inr",
                        "unit_amount": int(price2) * 100,
                        "product_data":{
                            "name":name
                        }
                        
                    },
                    "quantity": 1,
                }
            ],
           
            mode="payment",
            success_url=settings.PAYMENT_SUCCESS_URL,
            cancel_url=settings.PAYMENT_CANCEL_URL,
        )
        return redirect(checkout_session.url)
    
    
class SuccessView(TemplateView):
    template_name = 'cart/success.html'  # Replace 'success.html' with your success template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context data here if needed
        return context

class CancelView(TemplateView):
    template_name = "cart/cancel.html"