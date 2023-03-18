from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from . import forms

class LogoutView(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    template_name = "registration/home.html"
