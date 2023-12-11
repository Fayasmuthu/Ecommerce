from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import ContactForm,ApplicantForm
from .models import ContactMessage
from django.core.mail import send_mail
from django.views import View



# Create your views here.
class AboutView(TemplateView):
    template_name = 'products/details/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_about'] = True
        return context

    def get(self, request):
        form = ApplicantForm()
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)

    def post(self, request):
        form = ApplicantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success_page')  
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)

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

    else:
        form = ContactForm()
    
    # Add the form to the context dictionary
    context['form'] = form

    return render(request, 'products/details/contacts.html', context)


def blog(request):

    return render(request, 'products/details/blog.html',{'is_blog':True})
