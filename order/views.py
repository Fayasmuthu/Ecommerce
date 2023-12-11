
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from products.models import Store
from django.contrib.auth.models import User
from . models import Orders,OrderItem,UserProfile
from .forms import UserProfileForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.views import View
import stripe
from django.urls import reverse
from django.conf import settings
from django.views.generic import TemplateView

# Create your views here.
def index(request):
    return render(request, "index.html")

@login_required
def account_profile(request):
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
        'profile':profile
    }
    return render(request, 'account/account-profile.html', context)


@login_required
def account_order(request):
    user = request.user  # Get the current logged-in user
    orders = Orders.objects.filter(user=user)
    order_items = OrderItem.objects.filter(orders__in=orders)
    order_count = orders.count()
    profile = UserProfile.objects.get(user=request.user)



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
        'profile':profile

    }
    return render(request, "account/account-orders.html",context)


@login_required
def add_to_wishlist(request, store_id):
    store = Store.objects.get(id=store_id)
    if request.user in store.wishlisted_by.all():
        store.wishlisted_by.remove(request.user)
    else:
        store.wishlisted_by.add(request.user)

    return redirect('order:wishlist_page') 


@login_required
def wishlist_page(request):
    wishlist_items = request.user.wishlist.all()
    wishlist_count = request.user.wishlist.count()
    profile = UserProfile.objects.get(user=request.user)

    context = {
        'wishlist_items': wishlist_items,
        'wishlist_count': wishlist_count,
        'profile':profile

    }
    return render(request, 'account/wishlist.html',context)

  

@login_required
def cart_add(request, id):
    cart = Cart(request)
    product = Store.objects.get(id=id)
    cart.add(product=product)
    return redirect("products:shop")


@login_required
def item_clear(request, id):
    cart = Cart(request)
    product = Store.objects.get(id=id)
    cart.remove(product)
    return redirect("order:cart_detail")


@login_required
def item_increment(request, id):
    cart = Cart(request)
    product = Store.objects.get(id=id)
    cart.add(product=product)
    return redirect("order:cart_detail")


@login_required
def item_decrement(request, id):
    cart = Cart(request)
    product = Store.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("order:cart_detail")


@login_required
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("order:cart_detail")


@login_required
def cart_detail(request):
    profile = UserProfile.objects.get(user=request.user)
    cart_items = request.session.get('cart', {})
    
    # Calculate total cart amount
    cart_total_amount = sum(item['price'] * item['quantity'] for item in cart_items.values())

    context = {
        'cart_items': cart_items,
        'cart_total_amount': cart_total_amount,
        'profile':profile
    }
    return render(request, 'cart/cart.html',context)


@login_required
def checkout_detail(request):
    profile = UserProfile.objects.get(user=request.user)
    cart_items = request.session.get('cart', {})

    cart_total_amount = sum(item['price'] * item['quantity'] for item in cart_items.values())
    print("Cart Total Amount:", cart_total_amount) 

    context = {
        'cart_items': cart_items,
        'cart_total_amount': cart_total_amount,
        'profile':profile
    }
    return render(request, 'cart/checkout-details.html',context)


@login_required
def checkout_shipping(request):
    profile = UserProfile.objects.get(user=request.user)

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
        # return redirect(reverse('order:create-checkout-session', kwargs={'pk': order_id}))
           
    return render(request, 'cart/checkout-shipping.html',{'profile':profile})


def checkout_payment(request):
    profile = UserProfile.objects.get(user=request.user)
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
        'pk': pk 
    }
    return render(request, 'cart/checkout-payment.html',context)


def checkout_review(request):
    profile = UserProfile.objects.get(user=request.user)
    cart_items = request.session.get('cart', {})
    
    # Calculate total cart amount
    cart_total_amount = sum(item['price'] * item['quantity'] for item in cart_items.values())
    
    print("Cart Total Amount:", cart_total_amount)  # Add this line for debugging

    context = {
        'cart_items': cart_items,
        'cart_total_amount': cart_total_amount,
        'profile':profile

    }
    return render(request, 'cart/checkout-review.html',context)


def checkout_complete(request):
    return render(request, 'cart/checkout-complete.html')





class CreateStripeCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        cart_items = request.session.get('cart', {})
        cart_total_amount = sum(item['price'] * item['quantity'] for item in cart_items.values())
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": int(cart_total_amount * 100),  # Amount in cents
                        "product_data": {
                            "name": "Your Product Name",
                            "description": "Product Description",
                        },
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url = reverse('success'),
            cancel_url=request.build_absolute_uri(reverse("payment_cancel")),
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