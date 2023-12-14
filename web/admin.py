from django.contrib import admin
from .models import ContactMessage,Applicant



# Register your models here.
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'message')


class ApplicantAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']  # Customize fields to display in the admin list view

admin.site.register(Applicant, ApplicantAdmin)