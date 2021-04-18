from django import forms
from .models import Comment, NewsletterSubscription

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['content']
		widgets = {
			'content': forms.Textarea(
				attrs={
				'class': 'form-control ml-1 shadow-none textarea',
				'placeholder': 'Add a new comment...'
			})
		}

class EmailSubscriptionForm(forms.ModelForm):
  class Meta:
    model = NewsletterSubscription
    fields = ['email']
    widgets = {
    	'email': forms.TextInput(attrs={
		    'class': 'form-control',
		    'placeholder': 'Type your email address here...'
		  })
    }

class EmailUnsubscriptionForm(forms.Form):
  email = forms.EmailField(widget=forms.TextInput(
    attrs={
      'class': 'form-control w-50',
      'placeholder': 'Type your email address here...'
    }
  ))

# class EmailForm(forms.Form):
#     subject = forms.CharField(label='Subject')
#     to_email = forms.CharField(label='To')
#     message = forms.CharField(label='Message', widget=forms.Textarea())

#     def __init__(self, *args, **kwargs):
#         super(EmailForm, self).__init__(*args, **kwargs)
#         for field_name in self.fields.keys():
#             self.fields[field_name].widget.attrs.update({'class': 'form-control'})