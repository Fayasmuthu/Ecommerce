from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.
from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField()

    def __str__(self):
        return self.name  # Customize as needed
    

class Applicant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=128,blank=True,null=True)
    message = models.TextField()
    cv = models.FileField(upload_to='cv_uploads/')

    class Meta:
        verbose_name = ('About')
        verbose_name_plural = ('About')


    def __str__(self):
        return str("Change Your About")