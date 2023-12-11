from django.contrib import admin
from .models import ContactMessage,Applicant



# Register your models here.
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'message')

admin.site.register(Applicant)