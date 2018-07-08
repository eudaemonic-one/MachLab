"""
Definition of urls for Models.
"""

from Models import views as models_view
from django.conf.urls import include, url

urlpatterns = [
    # Models Pages #
    url(r'^(.*?)/(.*?)$', models_view.models, name='models'),
    url(r'^(.*?)/(.*?)/issues$', models_view.issues, name='issues'),
    url(r'^(.*?)/(.*?)/insights$', models_view.insights, name='insights'),
    url(r'^upload$', models_view.upload, name='upload'),
    url(r'^download$', models_view.download, name='download'),
    url(r'^new', models_view.new, name='new'),
    url(r'^drop$', models_view.drop, name='drop'),
]


