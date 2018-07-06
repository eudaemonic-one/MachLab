"""
Definition of urls for Models.
"""

from Models import views as models_view
from django.conf.urls import include, url

urlpatterns = [
    # Models Pages #
    url(r'^$', models_view.models, name='models'),
]


