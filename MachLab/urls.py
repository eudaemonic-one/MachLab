"""
Definition of urls for MachLab.
"""

from MachLab import view
from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Admin Console Panel #
    url('admin/', admin.site.urls),
    url('admin/doc/', include('django.contrib.admindocs.urls')),
    
    # Website Pages #
    url('', view.index),
    url('index/', view.index),

    # Model Lab#
    #url('ModelLab/', include('MachLab.ModelLab.urls')),
]
