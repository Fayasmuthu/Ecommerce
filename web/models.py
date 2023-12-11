from django.db import models

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
    email = models.EmailField()
    message = models.TextField()
    cv = models.FileField(upload_to='cv_uploads/')

    def __str__(self):
        return self.name