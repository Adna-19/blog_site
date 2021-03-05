from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

class ProfileManager(UserManager):
	def top_three_content_creators(self):
		users = self.all()
		top_three_users = sorted(users, key=lambda user: user.posts.count(), reverse=True)[:3]
		return top_three_users

class UserProfile(AbstractUser):

	GENDER_CHOICES = (
		('male', 'Male'),
		('female', 'Female'),
	)

	image = models.ImageField(upload_to='profile-images/', null=True, blank=True)
	gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
	bio = models.TextField(null=True, blank=True)
	about_user = models.TextField(null=True, blank=True)
	facebook_profile = models.URLField(null=True, blank=True)
	instagram_profile = models.URLField(null=True, blank=True)
	twitter_profile = models.URLField(null=True, blank=True)
	
	objects = ProfileManager()

	@property
	def full_name(self):
		return f"{self.first_name} {self.last_name}"

	def __str__(self):
		return self.full_name