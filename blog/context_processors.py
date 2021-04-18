from django.db.models import Q
from .models import Category, Post
from .forms import  EmailSubscriptionForm
from taggit.models import Tag

def get_all_categories(request):
  context = {'categories': Category.objects.all()}
  return context

def get_top_trending_posts(request):
  # Top trending posts for displaying on banner
  context = {'trending_posts': Post.objects.comments_greater_than(10)}
  return context

def get_most_commented_posts(request):
	most_commented_posts = Post.objects.comments_greater_than(5)
	context = {'most_commented_posts': most_commented_posts}
	return context

def get_all_tags(request):
	context = {'tags': Tag.objects.all()}
	return context

def email_subscription_form(request):
	context = {'newsletter_form': EmailSubscriptionForm()}
	return context