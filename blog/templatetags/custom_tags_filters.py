from django import template
from django.template.defaultfilters import stringfilter
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe
import markdown2
from ..models import SavedPost

register = template.Library()

@register.filter(is_safe=True)
@stringfilter
def markdown(value):
    extras = ["fenced-code-blocks"]
    return mark_safe(markdown2.markdown(force_str(value), extras=extras))
                
@register.filter()
def is_not_saved(post, user):
    if user.is_authenticated:
        try:
            saved_posts = user.collection.posts.all()
            if post in saved_posts: return False
        except ObjectDoesNotExist:
            SavedPost.objects.create(creator=user)
    return True

@register.filter()
def already_liked(object_, person):
    persons_already_liked_post = [like.liked_by for like in object_.likes.all()]
    if person in persons_already_liked_post:
        return True
    return False