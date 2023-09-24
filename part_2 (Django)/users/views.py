from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from allauth.account.views import SignupView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin  # Додайте імпорт
from users.models import CustomUser


class HomePageView(LoginRequiredMixin, TemplateView):  # Використовуйте LoginRequiredMixin
    template_name = 'users/home.html'


class CustomLoginView(LoginView):
    template_name = 'users/login.html'


class CustomLogoutView(LogoutView):
    next_page = 'users:home'


class CustomSignupView(SignupView):
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users:login')


class AuthorCreateView(LoginRequiredMixin, CreateView):
    model = author
    fields = ['fullname', 'born_date', 'born_location', 'description']
    template_name = 'users/author_form.html'
    success_url = reverse_lazy('authors')


class AuthorDetailView(DetailView):
    model = author
    template_name = 'users/author_detail.html'
