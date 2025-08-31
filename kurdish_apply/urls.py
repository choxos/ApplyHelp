"""
URL configuration for kurdish_apply project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _


urlpatterns = [
    # Language selection (outside i18n patterns)
    path('i18n/', include('django.conf.urls.i18n')),
    path('rosetta/', include('rosetta.urls')),  # Translation interface
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    
    # Main app URLs
    path('', include('accounts.urls')),
    path('destinations/', include('destinations.urls')),
    path('resume/', include('resume_builder.urls')),
    path('communications/', include('communications.urls')),
    path('resources/', include('resources.urls')),
    
    # Root path redirects to home
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    
    prefix_default_language=False
)

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])