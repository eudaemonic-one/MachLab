"""
Definition of urls for MachLab.
"""

from MachLab import view, settings
from Account import views as account_view
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Admin Console Panel #
    url(r'^admin/', admin.site.urls),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    # Search Pages #
    url(r'^search/', include('Search.urls')),

    # Docs Pages #
    url(r'^docs/', include('Docs.urls')),

    # Models Pages #
    url(r'^models/', include('Models.urls')),

    # Account Pages #
    url(r'^account/', include('Account.urls')),
    
    # Download Pages #
    url(r'^download/', view.download, name='download'),
    
    # User Profile Pages #
    url(r'^(.*?)/$', account_view.user_profile, name='user-profile'),
    
    # Website Pages #
    url(r'^$', view.index, name='index'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)