from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Orders(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    first_Name=models.CharField(max_length=50)
    last_Name=models.CharField(max_length=50)
    email =models.EmailField()
    phone=models.IntegerField()
    company=models.CharField(max_length=200,null=True,blank=True)
    country=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    postcode=models.IntegerField()
    address=models.TextField()
    address1=models.TextField()
    date_purchased = models.DateField(auto_now_add=True)


class OrderItem(models.Model):
    STATUS_CHOICES = [
        ('In Progress', 'In Progress'),
        ('Canceled', 'Canceled'),
        ('Delayed', 'Delayed'),
        ('Delivered', 'Delivered'),
    ]
    orders=models.ForeignKey(Orders,on_delete=models.CASCADE)
    store=models.CharField(max_length=50)
    image=models.ImageField(upload_to='media/order_image')
    quantity=models.IntegerField()
    price=models.FloatField()
    date_purchased = models.DateField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, default='In Progress', max_length=100)
    total=models.IntegerField()
    paid=models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    # Add any other fields you need

    def __str__(self):
        return self.user.username
    
    
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        # If UserProfile doesn't exist, create it
        UserProfile.objects.create(user=instance)



