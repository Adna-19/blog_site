from django.urls import path
from django.contrib.sitemaps.views import sitemap
from .sitemaps import PostSitemap
from . import views

app_name = 'blog'

urlpatterns = [
  path('', views.BlogListView.as_view(), name='home'),
  path('category/<slug:category_slug>/posts/', views.BlogListView.as_view(), name='list_by_category'),
  path('tag/<slug:tag_slug>/posts/', views.BlogListView.as_view(), name='list_by_tag'),
  path('post/<slug:slug>/', views.BlogDetailView.as_view(), name='post_detail'),
  path('post/<slug:slug>/like/', views.BlogPostLikeDisLikeView.as_view(), name='like_post'),
  path('create/', views.BlogPostCreateView.as_view(), name='create_post'),
  path('<int:pk>/edit/', views.BlogPostUpdateView.as_view(), name='update_post'),
  path('<slug:slug>/delete/', views.BlogPostDeleteView.as_view(), name='delete_post'),
  path('comment/<int:comment_id>/delete/', views.BlogPostCommentDeleteView.as_view(), name='delete_comment'),
  path('comment/<int:comment_id>/like/', views.PostCommentLikeDislikeView.as_view(), name='like_comment'),

  path('post/<slug:slug>/cms/details/', views.BlogPostContentsDetailView.as_view(), name='post_content_list'),
  path('post/<slug:slug>/contents/<model_name>/create/', views.PostContentCreateUpdateView.as_view(), name='create_content'),
  path('post/<slug:slug>/contents/<model_name>/<int:id>/update/', views.PostContentCreateUpdateView.as_view(), name='update_content'),
  path('post/<slug:slug>/content/<model_name>/<int:id>/delete/', views.PostContentDeleteView.as_view(), name='delete_content'),
  path('post/content/order/', views.PostContentOrderView.as_view(), name='order_content'),
]

sitemaps = {
  'posts': PostSitemap
}
urlpatterns += [path('sitemaps.xml/', sitemap, {'sitemaps': sitemaps}, name='sitemap'),]