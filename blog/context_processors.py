from django.db.models import Q
from .models import Category, Post

def get_all_categories(request):
  context = {'categories': Category.objects.all()}
  return context

def get_top_trending_posts(request):
  # Top trending posts for displaying on banner
  context = {'trending_posts': Post.objects.comments_greater_than(10)}
  return context