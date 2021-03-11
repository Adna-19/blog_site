from django.contrib.sitemaps import Sitemap 
from .models import Post

class PostSitemap(Sitemap):
  priority = 0.9
  changefreq = "monthly"

  def items(self):
    return Post.objects.published()

  def lastmod(self, obj):
    return obj.date_updated
