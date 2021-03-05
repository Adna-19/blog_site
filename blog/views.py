from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post, Category
from .forms import CommentForm

class BlogListView(ListView):
  model = Post
  paginate_by = 6
  template_name = 'blog/home.html'
  context_object_name = 'posts'
  category = None

  def dispatch(self, request, category_slug=None, *args, **kwargs):
    if category_slug:
      self.category = get_object_or_404(Category, slug=category_slug)
    return super(BlogListView, self).dispatch(request, category_slug, *args, **kwargs)

  def get_queryset(self):
    qs = super(BlogListView, self).get_queryset()
    if self.category:
      return qs.filter(category__title=self.category.title)
    return qs.filter(status='published')     

class BlogDetailView(TemplateResponseMixin, View):
  template_name = 'blog/details.html'

  def get(self, request, slug, *args, **kwargs):
    post = get_object_or_404(Post, slug=slug)
    form = CommentForm()
    return self.render_to_response({
      'post': post, 'form': form,
      'total_likes': post.likes.count()
    })

  def post(self, request, slug, *args, **kwargs):
    post = get_object_or_404(Post, slug=slug)
    form = CommentForm(request.POST)
    if form.is_valid():
      comment = form.save(commit=False)
      comment.post = post
      comment.author = request.user
      comment.save()
      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return self.render_to_response({'post': post, 'form': form})

class BlogPostLikeDisLikeView(View):
  def get(self, request, slug, *args, **kwargs):
    post = get_object_or_404(Post, slug=slug)
    list_of_persons_already_liked_post = [like.liked_by for like in post.likes.all()]
    if request.user in list_of_persons_already_liked_post:
      # dislike the post, if already liked.
      user_like = post.likes.get(liked_by=request.user)
      user_like.delete()
    else:
      post.likes.create(liked_by=request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class BlogPostCreateView(LoginRequiredMixin, CreateView):
  model = Post
  template_name = 'blog/post_creation_form.html'
  fields = [
    'title', 'category', 'image',
    'summary', 'status', 'content',
    'date_published',
  ]

  def form_valid(self, form):
    post = form.save(commit=False)
    post.author = self.request.user
    post.save()
    return super().form_valid(form)

class BlogPostUpdateView(LoginRequiredMixin, UpdateView):
  model = Post
  template_name = 'blog/post_update_form.html'
  fields = [
    'title', 'category', 'image',
    'summary', 'status', 'content',
    'date_published',
  ]

class BlogPostDeleteView(LoginRequiredMixin, DeleteView):
  model = Post
  success_url = reverse_lazy('blog:home')

