"""
Definition of urls for MachLab.
"""

from MachLab import view, settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Admin Console Panel #
    url(r'^admin/', admin.site.urls),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    # Website Pages #
    url(r'^$', view.index, name='index'),
    
    # Docs Pages #
    url(r'docs/', include('Docs.urls')),

    # Download Pages #
    url(r'download/', view.download, name='download'),

    # Account Pages #
    url(r'account/', include('Account.urls')),
    
    # Settings Pages #
    url(r'settings/', include('Settings.urls')),
    
    # Profile Pages #
    #url(r'(\S+)/', include('Profile.urls')),

    # Models Pages #
    url(r'models/', include('Models.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)