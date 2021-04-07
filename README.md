# Django powered blog_site

I created this Blog site using Django, Javascript. it consist of two Apps.

 - Accounts
 - Blog

## Accounts 
This app handles user accounts, their authentications , password change
and password reset functionalities. Well managed and bootstrap based templates
are used.

The Database model of the app consists of:

 - User inherited from AbstractUser

## Blog
This app has the core functionality for the Blog. it consists of all the basic 
building blocks to build a blog.

The Database model of the app consists of:

- Post Category
- Post Managers
- Comments
- Content (for diverse content)
- BaseContent (Abstract model)
- Text
- Image
- Likes
- Author of Post
- Saved Post

The likes model of the Blog is created using Generic relationships in Django. its very interesting
concept for modeling polymorphic models in Django DB.

All views in the blog app are Class-based views.

The project also contains sitemaps for the blog-app.

## Future Work
 - Newsletter  
 - Feeds