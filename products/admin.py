from django.contrib import admin
from products.models import(
    Maincategory,Groupcategory,Category,Subcategory,Store,Brand,Color,
    Size,AvaliableSize,ProductImage,Offer_sale,Review,Hero,offer_counter,
    Gallery_preview
)
# Register your models here.
@admin.register(Maincategory)
class MaincategoryAdmin(admin.ModelAdmin):
    list_display=('title',)
    prepopulated_fields={'slug': ('title',)}

@admin.register(Groupcategory)
class MaincategoryAdmin(admin.ModelAdmin):
    list_display=('title',)
    prepopulated_fields={'slug': ('title',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=('title',)
    prepopulated_fields={'slug': ('title',)}

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display=('title',)
    prepopulated_fields={'slug': ('title',)}
    list_filter = ("title",'category' )
    # autocomplete_fields = ("Category",)
    search_fields = (
        "title",
        'category__title',
    )

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display=('name',)
    search_fields = ('name',)

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display=('name','code')
    search_fields = ('name',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display=('name',)
    search_fields = ('name',)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0

class Gallery_previewInline(admin.TabularInline):
    model = Gallery_preview
    extra = 0
    
class AvailableSizeInline(admin.TabularInline):
    model = AvaliableSize
    extra = 0
    autocomplete_fields = ('size',)

class Offer_saleInline(admin.TabularInline):
    model = Offer_sale
    extra = 0

class offer_counterInline(admin.TabularInline):
    model = offer_counter
    extra = 0
   
@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'subcategory',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('subcategory', 'name',)
    inlines = [ProductImageInline, AvailableSizeInline,Offer_saleInline,
               offer_counterInline,Gallery_previewInline]
    autocomplete_fields = ("subcategory", "brand",)
    search_fields = (
        "name",
        'subcategory__name',
    )
    list_editable = ('subcategory',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['store', 'name', 'rating', 'email', 'created_at']
    list_filter = ['rating']
    search_fields = ['name', 'email']

admin.site.register(Hero)

