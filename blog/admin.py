from django.contrib import admin
from .models import Post, Comment, Category, SavedPost, Like

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ['title', 'content', 'slug']

class CommentInline(admin.StackedInline):
	model = Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ['title', 'slug', 'author', 'date_published', 'status']
	list_filter = ['author', 'category', 'status']
	inlines = [CommentInline]

admin.site.register(SavedPost)
admin.site.register(Like)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ['post', 'author', 'content']
	list_filter = ['author', 'post']