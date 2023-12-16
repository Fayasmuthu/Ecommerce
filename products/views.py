from django.shortcuts import render, redirect
from .models import (
    Maincategory,Groupcategory,Category,Subcategory,Store,Color,Brand,
    Size,Review,Hero
)
from django.views.generic import ListView ,TemplateView ,DetailView
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from .forms import ReviewForm
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from order.models import UserProfile
from django.shortcuts import get_object_or_404



# Create your views here.
def index(request):
    profile = UserProfile.objects.get(user=request.user)
    main_category = Maincategory.objects.all()
    group_category =Groupcategory.objects.all()
    categories = Category.objects.all()  
    subcategory = Subcategory.objects.all()
    store = Store.objects.all()
    offer_sale =Store.objects.filter(is_laptop=True)[:8]
    led_tv =Store.objects.filter(is_led_tv=True)[:8]
    kitchen_appliance =Store.objects.filter(is_kitchen_appliances=True)[:8]
    refrigentor =Store.objects.filter(is_home_appliances=True)[:8]
    air_condition =Store.objects.filter(is_air_conditions=True)[:8]
    computer_a_printers =Store.objects.filter(is_computer_a_printers=True)[:8]
    hero=Hero.objects.all()
    offer_counter =Store.objects.filter(is_offer_counter=True)[:8]
    best_seller =Store.objects.filter(is_best_seller=True)[:8]
    new_arrival =Store.objects.filter(is_new_arrival=True)[:8]
    top_rated =Store.objects.filter(is_top_rated=True)[:8]
    wishlist_count =request.user.wishlist.count()


    category=request.GET.get('category')
    q= request.GET.get('q')
    heros=request.GET.get('hero')
    
    if category:
        store = store.filter(subcategory__category__slug=category)

    if q :
        instance = Subcategory.objects.get(slug=q)
        store = store.filter(subcategory=instance)[:8]


    if heros:
       hero =hero.filter(hero__store__slug=heros)

    cart_items = request.session.get('cart', {})
    cart_total_amount = sum(item['price'] * item['quantity'] for item in cart_items.values())
    print("Cart Total Amount:", cart_total_amount)

    context ={
        'profile':profile,
        'main_category':main_category,
        'group_category':group_category,
        'categories': categories, 
        'subcategory':subcategory,
        'offer_sale':offer_sale,
        'led_tv':led_tv,
        'kitchen_appliance':kitchen_appliance,
        'refrigentor':refrigentor,
        'air_condition':air_condition,
        'computer_a_printers':computer_a_printers,
        'cart_items': cart_items,
        'cart_total_amount': cart_total_amount,
        'hero':hero,
        'offer_counter':offer_counter,
        'best_seller':best_seller,
        'new_arrival':new_arrival,
        'top_rated':top_rated,
        'wishlist_count': wishlist_count,
        "is_index": True

    }
    return render(request, "index.html",context)


def shop(request):
    profile = UserProfile.objects.get(user=request.user)
    main_category = Maincategory.objects.all()
    group_category =Groupcategory.objects.all()
    categories = Category.objects.all()  
    subcategory = Subcategory.objects.all()
    store = Store.objects.all()
    colors=Color.objects.all()
    brands =Brand.objects.annotate(store_count=Count('brand__name'))
    sizes =Size.objects.all()
    total_products = store.count()
    wishlist_count =request.user.wishlist.count()

    q= request.GET.get('q')
    category=request.GET.get('category')

    if q :
        instance = Subcategory.objects.get(slug=q)
        store = store.filter(subcategory=instance)

    if category:
        store = store.filter(subcategory__category__slug=category)

    cart_items = request.session.get('cart', {})
    cart_total_amount = sum(item['price'] * item['quantity'] for item in cart_items.values())
    print("Cart Total Amount:", cart_total_amount)  # Add this line for debugging

    query =request.GET.get('query')
    if query:
        store=Store.objects.filter(name__icontains=query)
    #_________________-END SEARCH-_________________________

    #__________________-PAGINATION-_______________________
    paginator = Paginator(store, 9)  

    page_number = request.GET.get('page')
    try:
        paginated_stores = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_stores = paginator.page(1)
    except EmptyPage:
        paginated_stores = paginator.page(paginator.num_pages) 

     #__________________-END PAGINATION-_______________________

    context ={
        'profile':profile,
        'main_category':main_category,
        'group_category':group_category,
        'categories': categories,
        'subcategory':subcategory,
        'stories':store,
        'colors':colors,
        'brands':brands,
        'sizes': sizes,
        'stars': range(1, 6),
        'cart_items': cart_items,
        'cart_total_amount': cart_total_amount,
        'stories': paginated_stores,
        'total_products': total_products,
        'wishlist_count': wishlist_count,
        "is_shop": True
   
    }

    return render(request, "products/details/shop.html",context)

def shop_list(request):
    profile = UserProfile.objects.get(user=request.user)
    main_category = Maincategory.objects.all()
    group_category =Groupcategory.objects.all()
    categories = Category.objects.all()  
    subcategory = Subcategory.objects.all()
    store = Store.objects.all()
    colors=Color.objects.all()
    brands =Brand.objects.annotate(store_count=Count('brand__name'))
    sizes =Size.objects.all()
    total_products = store.count()

    q= request.GET.get('q')
    category=request.GET.get('category')

    if q :
        instance = Subcategory.objects.get(slug=q)
        store = store.filter(subcategory=instance)

    if category:
        store = store.filter(subcategory__category__slug=category)

    cart_items = request.session.get('cart', {})
    cart_total_amount = sum(item['price'] * item['quantity'] for item in cart_items.values())
    print("Cart Total Amount:", cart_total_amount)  # Add this line for debugging

    query =request.GET.get('query')
    if query:
        store=Store.objects.filter(name__icontains=query)

    # #_________________-END SEARCH-_________________________

    #__________________-PAGINATION-_______________________
    paginator = Paginator(store, 5) 

    page_number = request.GET.get('page')
    try:
        paginated_stores = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_stores = paginator.page(1)  # If page is not an integer, show first page
    except EmptyPage:
        paginated_stores = paginator.page(paginator.num_pages)  # If page is out of range, show last page

     #__________________-END PAGINATION-_____________________________
    

    context ={
        'profile':profile,
        'main_category':main_category,
        'group_category':group_category,
        'categories': categories,
        'subcategory':subcategory,
        'stories':store,
        'colors':colors,
        'brands':brands,
        'sizes': sizes,
        'stars': range(1, 6),
        'cart_items': cart_items,
        'cart_total_amount': cart_total_amount,
        'stories': paginated_stores,
        'total_products': total_products,
    }

    return render(request, "products/details/shop-list.html",context)


def filter_data(request):
    selected_brand = request.GET.getlist('brands[]')
    print("Selected Brands:", selected_brand)  # Add this line for debugging

    if selected_brand:
        course = Store.objects.filter(brand__id__in = selected_brand).order_by('-id')
    else:
        course = Store.objects.all().order_by('-id')

    t = render_to_string('ajax/store.html', {'course': course})
    return JsonResponse({'data': t})

def filter_data_list(request):
    selected_brand = request.GET.getlist('brands[]')
    print("Selected Brands:", selected_brand)  # Add this line for debugging

    if selected_brand:
        course = Store.objects.filter(brand__id__in = selected_brand).order_by('-id')
    else:
        course = Store.objects.all().order_by('-id')

    t = render_to_string('ajax/store_list.html', {'course': course})
    return JsonResponse({'data': t})


def filter_products_by_price(request):
    if request.is_ajax() and request.method == 'GET':
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        # Filter products by price range
        filtered_products = Store.objects.filter(avaliablesize__orginal_price__gte=min_price, avaliablesize__orginal_price__lte=max_price).distinct()

        # Prepare data to send back as a JSON response
        data = {
            'data': render_to_string('ajax/product_list.html', {'filtered_products': filtered_products})
        }
        return JsonResponse(data)


class products_detailsViews(DetailView):
    model = Store
    template_name = 'products/details/shop-single.html'
    context_object_name = 'store'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        store=context['store']
        overall_rating = 3.5  # Replace this with your actual overall rating value
        reviews = Review.objects.filter(store=store)
        # reviews = Review.objects.filter(store=store).select_related('store').values('found_helpful_percentage', 'other_fields')

        total_reviews =reviews.count()
        if total_reviews >0:
            average_rating =sum([review.rating for review in reviews]) / total_reviews
        else:
            average_rating=0

        star_counts = {
        '5': reviews.filter(rating=5).count(),
        '4': reviews.filter(rating=4).count(),
        '3': reviews.filter(rating=3).count(),
        '2': reviews.filter(rating=2).count(),
        '1': reviews.filter(rating=1).count(),
    }
        
        context['review_form']=ReviewForm()
        context['average_rating'] = round(average_rating, 1)
        context['total_reviews'] = total_reviews
        context['star_counts'] = star_counts
        context['stars'] = range(1, 6) 
        context['overall_rating'] = overall_rating
        context['profile']=UserProfile

        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        context['profile'] = user_profile

        return context
    
    def post(self,request,*args, **kwargs):
        store =self.get_object()
        form =ReviewForm(request.POST)

        if form.is_valid():
            review =form.save(commit=False)
            review.store =store
            review.save()
            return redirect('products:products_details',slug=store.slug)
        
        context=self.get_context_data()
        context['review_form']=form
        return self.render_to_response(context)
    
