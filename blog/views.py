from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic.list import ListView
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.apps import apps
from django.urls import reverse_lazy
from django.forms.models import modelform_factory
from taggit.models import Tag
from braces.views import (
  CsrfExemptMixin, 
  JsonRequestResponseMixin, 
  JSONResponseMixin
)
from .models import Post, Category, Comment, Content, NewsletterSubscription
from accounts.models import UserProfile
from .newsletter_operations import subscribe, unsubscribe
from .forms import (
  CommentForm, 
  EmailSubscriptionForm, 
  EmailUnsubscriptionForm
)

class BlogListView(ListView):
  model = Post
  paginate_by = 6
  template_name = 'blog/home.html'
  context_object_name = 'posts'
  category = None
  tag = None

  def dispatch(self, request, category_slug=None, tag_slug=None, *args, **kwargs):
    if category_slug:
      self.category = get_object_or_404(Category, slug=category_slug)
    if tag_slug:
      self.tag = get_object_or_404(Tag, slug=tag_slug)    
    return super(BlogListView, self).dispatch(request, category_slug, *args, **kwargs)

  def get_queryset(self):
    qs = super(BlogListView, self).get_queryset()
    if self.category:
      return qs.filter(category__title=self.category.title)
    elif self.tag:
      return qs.filter(tags__name=self.tag)
    return qs.filter(status='published')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['top_content_creators'] = UserProfile.objects.top_three_content_creators()
    # context['form'] = EmailSubscriptionForm()
    return context

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

class BlogPostContentsDetailView(DetailView):
  # detail view for content creator
  model = Post
  template_name = 'cms/post_detail.html'
  context_object_name = 'post'

class BlogPostLikeDisLikeView(View):
  def get(self, request, slug, *args, **kwargs):
    post = get_object_or_404(Post, slug=slug)
    list_of_persons_already_liked_post = [like.liked_by for like in post.likes.all()]
    if request.user in list_of_persons_already_liked_post:
      # dislike the post, if already liked.
      user_like = post.likes.get(liked_by=request.user)
      user_like.delete()
      action = 'disliked'
    else:
      post.likes.create(liked_by=request.user)
      action = 'liked'
    return JsonResponse({'action': action})

class PostCommentLikeDislikeView(View):
  def get(self, request, comment_id, *args, **kwargs):
    comment = get_object_or_404(Comment, id=comment_id)
    list_of_persons_already_liked_comment = [like.liked_by for like in comment.likes.all()]

    if request.user in list_of_persons_already_liked_comment:
      # dislike the comment, if already_liked
      user_like = comment.likes.get(liked_by=request.user)
      user_like.delete()
      action = 'disliked'
    else:
      comment.likes.create(liked_by=request.user)
      action = 'liked'
    return JsonResponse({'action': action})

class BlogPostCommentDeleteView(LoginRequiredMixin, View):
  def get(self, request, comment_id, *args, **kwargs):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    comment.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
  
class BlogPostCreateView(LoginRequiredMixin, CreateView):
  model = Post
  template_name = 'blog/post_creation_form.html'
  post_id = None
  fields = [
    'title', 'category', 'image',
    'summary', 'status',
    'date_published',
  ]

  def form_valid(self, form):
    post = form.save(commit=False)
    post.author = self.request.user
    post.save()
    # holding new post's id for redirecting to content_list page of that post
    self.post_id = post.id
    return super().form_valid(form)

  def get_success_url(self):
    post_slug = get_object_or_404(Post, id=self.post_id).slug
    return reverse_lazy('blog:post_content_list', kwargs={'slug': post_slug})

class PostContentCreateUpdateView(TemplateResponseMixin, View):
  template_name = 'cms/content_form.html'
  model         = None
  blog_post     = None
  obj           = None

  def get_content_model(self, model_name):
    if model_name in ('text', 'image'):
      return apps.get_model(app_label='blog', model_name=model_name)
    return None

  def get_form(self, model, *args, **kwargs):
    Form = modelform_factory(model, exclude=['owner', 'order', 'date_created', 'date_updated'])
    return Form(*args, **kwargs)

  def dispatch(self, request, slug, model_name, id=None, *args, **kwargs):
    self.blog_post  = get_object_or_404(Post, slug=slug, author=request.user)
    self.model = self.get_content_model(model_name)

    if id:
      self.obj = get_object_or_404(self.model, id=id, owner=request.user)
    return super(PostContentCreateUpdateView, self).dispatch(request, slug, model_name, id, *args, **kwargs)

  def get(self, request, slug, model_name, id=None, *args, **kwargs):
    form = self.get_form(self.model, instance=self.obj)
    return self.render_to_response({'form': form, 'object': self.obj})

  def post(self, request, slug, model_name, id=None, *args, **kwargs):
    form = self.get_form(self.model, instance=self.obj, data=request.POST, files=request.FILES)

    if form.is_valid():
      content = form.save(commit=False)
      content.owner = request.user
      content.save()

      if not id:
        # create new content object
        Content.objects.create(post=self.blog_post, content_object=content)
      return redirect('blog:post_content_list', self.blog_post.slug)
    return self.render_to_response({'form': form, 'object': self.obj})

class PostContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
  def post(self, request, *args, **kwargs):
    for object_id, order in self.request_json.items():
      Content.objects.filter(
        id=int(object_id),
        post__author=request.user
      ).update(order=order)
    return self.render_json_response({'message': 'Reordered successfully'})

class PostContentDeleteView(LoginRequiredMixin, View):

  def get_content_model(self, model_name):
    if model_name in ('text', 'image'):
      return apps.get_model(app_label='blog', model_name=model_name)
    return None

  def get(self, request, slug, model_name, id, *args, **kwargs):
    if request.is_ajax:
      post = get_object_or_404(Post, slug=slug, author=request.user)
      model = self.get_content_model(model_name)

      content = post.contents.get(id=id, content_type__model=model_name)
      content_item = get_object_or_404(model, id=content.content_object.id, owner=request.user)

      # delete both the content_type and content_object
      content.delete(); content_item.delete()
      return JsonResponse({'message': 'Content deleted successfully'})
    return JsonResponse({'message': 'Something went wrong'})


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


# NEWSLETTER VIEWS

class EmailSubscriptionView(JSONResponseMixin, View):
  json_dumps_kwargs = {u"indent": 2}

  def post(self, request, *args, **kwargs):
    form = EmailSubscriptionForm(request.POST or None)

    if form.is_valid():
      email_already_exists = NewsletterSubscription.objects.filter(
        email=form.cleaned_data.get('email')).exists()

      if email_already_exists:
        return self.render_json_response({
          'message': 'You are already subcribed to our Blog', 
          'header': 'Already Subscribed!', 
          'type': 'warning'
        })
      
      subscribe(form.cleaned_data.get('email'))
      form.save()
      return self.render_json_response({
          'message': 'you have successfully subscribed to Our Blog', 'header': 'Thank you! for Subscribing', 
          'type': 'success'
        })

    return self.render_json_response({'error': form.errors})

class EmailUnsubscriptionView(TemplateResponseMixin, View):
  template_name = 'blog/unsubscribe_newsletter.html'

  def get(self, request, *args, **kwargs):
    form = EmailUnsubscriptionForm()
    return self.render_to_response({'form': form})

  def post(self, request, *args, **kwargs):
    form = EmailUnsubscriptionForm(request.POST)
    if form.is_valid():
      subscription = get_object_or_404(NewsletterSubscription, 
        email=form.cleaned_data.get('email'))
      unsubscribe(subscription.email)
      # after unsubscribing from mailchimp, delete subscription from model.
      subscription.delete()
      return redirect('blog:home')
    return self.render_to_response({'form': form})


