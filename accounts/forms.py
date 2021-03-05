from django import forms
from .models import UserProfile

class SignUpForm(forms.ModelForm):
  password = forms.CharField(widget=forms.PasswordInput(
    attrs={'placeholder': 'password'}
  ))
  password2 = forms.CharField(widget=forms.PasswordInput(
    attrs={'placeholder': 'confirm password'}
  ))

  def __init__(self, *args, **kwargs):
    super(SignUpForm, self).__init__(*args, **kwargs)

    for field_name in self.fields.keys():
      print(field_name)
      self.fields[field_name].widget.attrs.update({
        'class': 'form-control mb-3',
      })

  class Meta:
    model = UserProfile
    fields = [
      'username', 'first_name', 'last_name',
      'email', 'image', 'gender', 'bio', 'about_user',
      'facebook_profile', 'instagram_profile', 'twitter_profile'
    ]
    widgets = {
      'username': forms.TextInput(attrs={
        'placeholder': 'Username'
      }),
      'email': forms.TextInput(attrs={
        'placeholder': 'Email address'
      }),
      'first_name': forms.TextInput(attrs={
        'placeholder': 'First name'
      }),
      'last_name': forms.TextInput(attrs={
        'placeholder': 'Last name'
      }),
      'bio': forms.Textarea(attrs={
        'placeholder': 'Set a bio for your account'
      }),
      'about_user': forms.Textarea(attrs={
        'placeholder': 'Say something about your skills'
      }),
      'facebook_profile': forms.TextInput(attrs={
        'placeholder': 'FB Profile link',
        'style': 'width:17rem'
      }),
      'instagram_profile': forms.TextInput(attrs={
        'placeholder': 'Insta Profile link',
        'style': 'width:17rem'
      }),
      'twitter_profile': forms.TextInput(attrs={
        'placeholder': 'Twitter Profile link',
        'style': 'width:17rem'
      })
    }

class ProfileSettingsForm(forms.ModelForm):
  def __init__(self, *args, **kwargs):
    super(ProfileSettingsForm, self).__init__(*args, **kwargs)

    for field_name in self.fields.keys():
      print(field_name)
      self.fields[field_name].widget.attrs.update({
        'class': 'form-control mb-3',
      })

  class Meta:
    model = UserProfile
    fields = [
      'username', 'first_name', 'last_name',
      'email', 'gender', 'image', 'bio',
      'about_user', 'facebook_profile', 
      'instagram_profile', 'twitter_profile'
    ]
    widgets = {
      'facebook_profile': forms.TextInput(attrs={
        'style': 'width:17rem'
      }),
      'instagram_profile': forms.TextInput(attrs={
        'style': 'width:17rem'
      }),
      'twitter_profile': forms.TextInput(attrs={
        'style': 'width:17rem'
      })
    }