from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.views.generic.base import RedirectView, View, TemplateResponseMixin
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import PasswordChangeForm
from .models import UserProfile
from .forms import SignUpForm, ProfileSettingsForm

class LoginView(FormView):
  form_class = AuthenticationForm
  template_name = 'accounts/authentications/login.html'
  success_url = reverse_lazy('blog:home')

  def form_valid(self, form):
    cd = form.cleaned_data
    user = authenticate(username=cd['username'], password=cd['password'])
    login(self.request, user)
    return super(LoginView, self).form_valid(form)

class LogoutView(RedirectView):
  permanent = True
  query_string = True
  pattern_name = 'login'

  def get_redirect_url(self, *args, **kwargs):
    logout(self.request)
    return super(LogoutView, self).get_redirect_url(*args, **kwargs)

class SignUpView(CreateView):
  model = UserProfile
  template_name = 'accounts/authentications/signup.html'
  form_class = SignUpForm
  success_url = reverse_lazy('login')

  def form_valid(self, form):
    user = form.save(commit=False)
    user.set_password(form.cleaned_data['password2'])
    user.save()
    return super().form_valid(form)

class PasswordChangeView(TemplateResponseMixin, View):
  model = UserProfile
  template_name = 'accounts/authentications/password_change_form.html'

  def get(self, request, *args, **kwargs):
    form = PasswordChangeForm(request.user)
    return self.render_to_response({'form': form})

  def post(self, request, *args, **kwargs):
    form = PasswordChangeForm(request.user, request.POST)
    if form.is_valid():
      form.save()
      return redirect('login')

class ProfileSettingsView(UpdateView):
  template_name = 'accounts/authentications/profile_update_form.html'
  model = UserProfile
  form_class = ProfileSettingsForm
  success_url = reverse_lazy('blog:home')

  def form_valid(self, form):
    if form.is_valid():
      form.save()
    return super().form_valid(form)