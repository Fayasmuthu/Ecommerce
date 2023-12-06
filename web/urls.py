from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = "web"

urlpatterns = [
    # path("", views.index, name="index"),
    path("about/", TemplateView.as_view(template_name="products/details/about.html"), name="about"),
    path("contact/", views.contact, name="contact"),
    path("blog/", views.blog, name="blog"),

]