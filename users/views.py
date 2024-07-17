import os
import secrets

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, UpdateView, DeleteView, ListView

from users.forms import UserRegisterForm, UserUpdateForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/user_form.html'
    extra_context = {'title': 'Регистрация'}

    def form_valid(self, form):
        user = form.save()
        user.is_active = True
        user.set_password(user.password)
        user.save()

        return super().form_valid(form)
