from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import ContactForm,ApplicantForm
from .models import ContactMessage
from django.core.mail import send_mail
from django.views import View
from django.http import HttpResponse
from django.http import JsonResponse
import json


# Create your views here.
def about(request):
    form = ApplicantForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            response_data = {
                "status": "true",
                "title": "Successfully Submitted",
                "message": "Message successfully updated",
            }
        else:
            print(form.errors)
            response_data = {
                "status": "false",
                "title": "Form validation error",
                'error':form.errors
            }
        return HttpResponse(
            json.dumps(response_data), content_type="application/javascript"
        )
    else:
        context = {
            "is_about": True,
            "form": form,
        }

    return render(request, 'products/details/about.html', context)


def contact(request):
    context = {'is_contact': True} 

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            contact_message = ContactMessage.objects.create(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message
            )
            contact_message.save()

            # Sending an email using Django's send_mail function
            send_mail(
                f'{subject} - {name}',
                f'Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}',
                email,  # Sender's email (optional, can be set in settings.py)
                ['fayasmuthu45@gmail.com'],  # Recipient's email(s)
                fail_silently=False,
            )

            # Optionally, you can reset the form after successful submission
            form = ContactForm()
            response_data = {
                "status": "true",
                "title": "Successfully Submitted",
                "message": "Message successfully updated",
            }
        else:
            print(form.errors)
            response_data = {
                "status": "false",
                "title": "Form validation error",
                'error':form.errors
            }
        return HttpResponse(
            json.dumps(response_data), content_type="application/javascript"
        )

    else:
        form = ContactForm()
    
    # Add the form to the context dictionary
    context['form'] = form

    return render(request, 'products/details/contacts.html', context)


def blog(request):

    return render(request, 'products/details/blog.html',{'is_blog':True})
