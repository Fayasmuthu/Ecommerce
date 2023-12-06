from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
class AboutView(TemplateView):
    template_name = 'products/details/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional context data if needed
        context['is_about'] = True
        return context
    
def contact(request):

    return render(request, 'products/details/contacts.html',{'is_contact':True})

def blog(request):

    return render(request, 'products/details/blog.html',{'is_blog':True})
