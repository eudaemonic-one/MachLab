"""
Definition of urls for Search.
"""

from Search import views as search_view
from django.conf.urls import include, url

urlpatterns = [
    # Models Pages #
    url(r'^$', search_view.search, name='search'),
]
