from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from blog.views import EmailSubscriptionView, EmailUnsubscriptionView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('blog/', include('blog.urls', namespace='blog')),

    # EMAIL NEWSLETTER PATTERNS
    path('newsletter/subscribe/', EmailSubscriptionView.as_view(), name='subscribe'),
    path('newsletter/unsubscribe/', EmailUnsubscriptionView.as_view(), name='unsubscribe')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)