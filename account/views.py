from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView
from . import forms
from .models import User

# Create your views here.
class SignUp(CreateView):
    form_class = forms.UserCreateForm
    model = User
    success_url = reverse_lazy("login")
    template_name = "signup.html"
