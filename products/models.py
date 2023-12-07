from django.db import models
from colorfield.fields import ColorField
from django.core.validators import MaxValueValidator
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib.auth.models import User


class Maincategory(models.Model):
    title =models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    class Meta:
        ordering = ('id',)
        verbose_name = ('Main Category')
        verbose_name_plural = ('Main Categories')

    def __str__(self):
        return str(self.title)
    
class Groupcategory(models.Model):
    m_category =models.ForeignKey(Maincategory, on_delete=models.CASCADE, related_name='group_categories')
    title =models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    class Meta:
        ordering = ('id',)
        verbose_name = ('Group Category')
        verbose_name_plural = ('Group Categories')

    def __str__(self):
        return str(self.title + "--" + self.m_category.title + "--" + self.title)

class Category(models.Model):
    g_category =models.ForeignKey(Groupcategory, on_delete=models.CASCADE, related_name='categories')
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    image = models.ImageField(upload_to='category/image')
    n_offer =models.CharField(max_length=200)
    link =models.CharField(max_length=200)


    class Meta:
        ordering = ('id',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.g_category.m_category.title + "--" + self.g_category.title +"--"+ self.title


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    title = models.CharField(max_length=200)
    slug = models.SlugField()


    class Meta:
        ordering = ('id',)
        verbose_name = 'Subcategory'
        verbose_name_plural = 'Subcategories'

    def __str__(self):
        return self.title
    
    def get_product_count(self):
        return Store.objects.filter(subcategory=self).count()
    

class Brand(models.Model):
    name =models.CharField(max_length=100)
    slug =models.SlugField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    

class Color(models.Model):
    name =models.CharField(max_length=100)
    code =ColorField(default='#fff')

    def __str__(self):
        return self.name
    

class Size(models.Model):
    name =models.CharField(max_length=100)
    slug =models.SlugField()

    def __str__(self):
        return self.name
    
    
class Store(models.Model):
    STOCK=(('IN STOCK','IN STOCK'),('OUT OF STOCK','OUT OF STOCK'))

    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='stores')
    name = models.CharField(max_length=200)
    slug =models.SlugField()
    description =models.CharField(max_length=500)
    vendor =models.CharField(max_length=100)
    image =models.ImageField(upload_to='store/img')
    available=models.BooleanField(default=True)
    brand =models.ForeignKey(Brand,on_delete=models.CASCADE,related_name='brand', null=True, blank=True)
    rating =models.PositiveIntegerField(
        validators=[MaxValueValidator(5)],default=5,verbose_name='product Rating (max:5)'
    )
    stock =models.CharField(choices=STOCK, max_length=200)
    is_best_seller = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)
    is_top_rated = models.BooleanField(default=False)

    is_laptop =models.BooleanField(default=False)
    is_computer_a_printers =models.BooleanField(default=False)
    is_apple_store =models.BooleanField(default=False)
    is_led_tv =models.BooleanField(default=False)
    is_home_appliances =models.BooleanField(default=False)
    is_kitchen_appliances =models.BooleanField(default=False)
    is_air_conditions=models.BooleanField(default=False)
    is_gadgets =models.BooleanField(default=False)
    is_offer_counter =models.BooleanField(default=False)
    wishlisted_by = models.ManyToManyField(User, related_name='wishlist', blank=True)


    class Meta:
        ordering = ('id',)
        verbose_name = ('products ')
        verbose_name_plural = ('Product')

    def delete(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        super(Store, self).delete(*args, **kwargs)
        storage.delete(path)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_image(self):
        return ProductImage.objects.filter(store=self)
    
    def get_color(self):
        return ProductImage.objects.filter(store=self).distinct()
    
    def get_sizes(self):
        return AvaliableSize.objects.filter(store=self)
    
    def get_price(self):
        return min([p.price for p in self.get_sizes()])
    
    def get_original_price(self):
        sizes =self.get_sizes()
        Value_prices =[p.orginal_price for p in sizes if p.orginal_price is not None]
        return min(Value_prices)if Value_prices else None
    
    def get_absolute_url(self):
        return reverse("products:products_details", kwargs={"slug": self.slug})
    
    def related_store(self):
        return Store.objects.filter().exclude(pk=self.pk).distinct()[0:12]
    
    def get_offer_sale(self):
        return Offer_sale.objects.filter(store=self)
    
    def get_review(self):
        return Review.objects.filter(store=self)
    

class AvaliableSize(models.Model):
    store = models.ForeignKey(Store,on_delete=models.CASCADE, related_name='store')
    size =models.ForeignKey('products.Size', on_delete=models.CASCADE, null=True , blank=True)
    color =models.ForeignKey('products.Color', on_delete=models.CASCADE, null=True , blank=True)
    price =models.DecimalField(max_digits=10,decimal_places=0)
    orginal_price =models.IntegerField(null=True ,blank=True)
    opening_stock=models.IntegerField(null=True ,blank=True)
    mini_order_qty=models.IntegerField(null=True ,blank=True)

    class Meta:
        ordering = ("price",)
        verbose_name = ("Available Size")
        verbose_name_plural = ("Available Sizes")

class ProductImage(models.Model):
    store =models.ForeignKey(Store, on_delete=models.CASCADE,null=True,blank=True)
    name =models.CharField(max_length=200,null=True,blank=True)
    image=models.ImageField(upload_to='store/img2',null=True,blank=True)
    color =models.ForeignKey('products.Color',on_delete=models.CASCADE,null=True,blank=True)
    size =models.ForeignKey('products.Size',on_delete=models.CASCADE,null=True,blank=True)


    class Meta:
        ordering = ("store",)
        verbose_name = ("Product Image")
        verbose_name_plural = ("Product Images")

    def __str__(self):
        return str(self.name)
    
class Offer_sale(models.Model):
    store = models.ForeignKey(Store,on_delete=models.CASCADE)
    image =models.ImageField(upload_to='store/offer_sale', null=True,blank=True)

class Review(models.Model):
    store =models.ForeignKey(Store, on_delete=models.CASCADE)
    name =models.CharField(max_length=100)
    email =models.EmailField()
    rating =models.IntegerField()
    review_text =models.TextField(max_length=300)
    created_at =models.DateField(auto_now_add=True)

class Hero(models.Model):
    store =models.ForeignKey(Store, on_delete=models.CASCADE)
    title_hero =models.CharField(max_length=150,null=True ,blank=True)
    image_hero =models.ImageField(upload_to='img/hero',null=True ,blank=True)
    topic_hero =models.CharField(max_length=200,null=True ,blank=True)
    vendor_hero=models.CharField(max_length=200,null=True ,blank=True)

class offer_counter(models.Model):
    store =models.ForeignKey(Store, on_delete=models.CASCADE)
    image_hero =models.ImageField(upload_to='img/hero',null=True ,blank=True)
    title_with =models.CharField(max_length=150,null=True ,blank=True)
    topic_hero =models.CharField(max_length=200,null=True ,blank=True)
    with_title=models.CharField(max_length=200,null=True ,blank=True)
    sale_end_date = models.DateField(blank=True,null=True)
    


