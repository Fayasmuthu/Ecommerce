from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = "products"

urlpatterns = [
     path("", views.index, name="index"),
     path("shop", views.shop, name="shop"),
     path("shop_list", views.shop_list, name="shop_list"),
     path('details/<slug:slug>/',views.products_detailsViews.as_view(),name='products_details'),
     path('product/filter-data',views.filter_data, name="filter-data"),
     path('filter-data-list/', views.filter_data_list, name='filter-data-list'),
     path('filter-products-by-price/', views.filter_products_by_price, name='filter_products_by_price'),
]