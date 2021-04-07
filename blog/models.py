from django.db import models
from accounts.models import UserProfile
from taggit.managers import TaggableManager
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
from datetime import datetime
from .fields import OrderField

class Category(models.Model):
	title = models.CharField(max_length=100)
	slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
	content = models.TextField()

	class Meta:
		verbose_name_plural = 'Categories'

	def save(self, *args, **kwargs):
		date = datetime.now()
		self.slug = f"{slugify(self.title)}-{slugify(date)}"
		super(Category, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return f"/blog/{self.slug}/posts/"

	def __str__(self):
		return self.title

class PostManager(models.Manager):
	def published(self):
		return self.filter(status='published').order_by('-date_published')

	def comments_greater_than(self, value):
		posts = self.filter(status='published').order_by('-date_published')
		most_commented_posts = []
		for post in posts:
			if post.comments.count() >= value:
				most_commented_posts.append(post)
		return most_commented_posts

class Like(models.Model):
	liked_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True)

	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
	object_id = models.PositiveIntegerField(null=True)
	content_object = GenericForeignKey()

	def __str__(self):
		return f"{self.content_type} liked by {self.liked_by.username}"

class Post(models.Model):
	STATUS_CHOICES = (
		('published', 'Published'),
		('draft', 'Draft'),
	)

	author = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, related_name='posts', null=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
	title = models.CharField(max_length=255, null=True, blank=True)
	image = models.ImageField(upload_to='post-images/')
	slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
	summary = models.TextField()
	status = models.CharField(max_length=10, choices=STATUS_CHOICES)
	date_created = models.DateField(auto_now_add=True)
	date_updated = models.DateField(auto_now=True)
	date_published = models.DateField()
	# content = models.TextField()
	likes = GenericRelation(Like)

	tags = TaggableManager()
	objects = PostManager()

	def save(self, *args, **kwargs):
		date = datetime.now()
		self.slug = f"{slugify(self.title)}-{slugify(date)}"
		super(Post, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return f"/blog/post/{self.slug}/"

	def __str__(self):
		return self.title

class Content(models.Model):
	post = models.ForeignKey(Post, related_name='contents', on_delete=models.CASCADE)
	order = OrderField(blank=True, for_fields=['post'])

	content_type = models.ForeignKey(ContentType, 
																	on_delete=models.CASCADE, 
																	limit_choices_to={'model__in':('text', 'image')})
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey()

	class Meta:
		ordering = ['order']

class BaseContent(models.Model):
	title = models.CharField(max_length=200)
	owner = models.ForeignKey('accounts.UserProfile', related_name='%(class)s_related', on_delete=models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True

	def __str__(self):
		return self.title

class Text(BaseContent):
	text = models.TextField()

class Image(BaseContent):
	image = models.ImageField()

class SavedPost(models.Model):
	creator = models.OneToOneField(UserProfile, null=True, blank=True, on_delete=models.CASCADE, related_name='collection')
	posts = models.ManyToManyField(Post, related_name='saved_posts')

	def __str__(self):
		return f"posts saved by {self.creator.username}"

class Comment(models.Model):
	author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='comments')
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	content = models.TextField()
	active = models.BooleanField(default=True)
	date_created = models.DateField(auto_now_add=True)
	date_updated = models.DateField(auto_now=True)
	likes = GenericRelation(Like)

	def get_delete_url(self):
		return f"/blog/comment/{self.id}/delete/"

	class Meta:
		ordering = ['-date_created']

	def __str__(self):
		return f"by {self.author.username} on post '{self.post.title}'"