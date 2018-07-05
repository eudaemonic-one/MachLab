"""
Definition of urls for MachLab.
"""

from MachLab import view
from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Admin Console Panel #
    url(r'^admin/', admin.site.urls),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    # Website Pages #
    url(r'^$', view.index, name='index'),

    # Account Pages #
    url(r'account/', include('Account.urls')),

    # Docs Pages #
    url(r'docs/', include('Docs.urls')),

    # Download Pages #
    url(r'download/', view.download, name='download'),
]
