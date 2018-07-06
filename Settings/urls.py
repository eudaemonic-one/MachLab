"""
Definition of urls for Settings.
"""

from Settings import views as settings_view
from django.conf.urls import include, url

urlpatterns = [
    # Settings Pages #
    url(r'profile/', settings_view.profile, name='profile'),
    url(r'account/', settings_view.account, name='account'),
    url(r'repositories/', settings_view.repositories, name='repositories'),
    url(r'applications/', settings_view.applications, name='applications'),
]


