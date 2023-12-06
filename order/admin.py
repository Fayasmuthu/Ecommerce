from django.contrib import admin

# Register your models here.
from .models import OrderItem,Orders,UserProfile

class OrderitemTubleInline(admin.TabularInline):
    model=OrderItem
class OrderAdmin(admin.ModelAdmin):
    inlines=[OrderitemTubleInline]

admin.site.register(Orders,OrderAdmin),
admin.site.register(OrderItem),


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'email', 'phone_number', 'image']

