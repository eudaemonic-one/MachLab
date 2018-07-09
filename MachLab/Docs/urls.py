"""
Definition of urls for Docs.
"""

from Docs import views as docs_view
from django.conf.urls import include, url

urlpatterns = [
    # Docs Pages #
    url(r'^$', docs_view.docs, name='docs'),
    url(r'overview/', docs_view.overview, name='overview'),
    url(r'setup/', docs_view.setup, name='setup'),
    url(r'userguide/', docs_view.userguide, name='userguide'),
    url(r'supporting/faq', docs_view.faq, name='faq'),
]

