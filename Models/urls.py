"""
Definition of urls for Models.
"""

from Models import views as models_view
from django.conf.urls import include, url

urlpatterns = [
    # Models Pages #
    url(r'^(.*?)/(.*?)/(.*?)/$', models_view.modelfile),
    url(r'^(.*?)/(.*?)/$', models_view.models, name='models'),
    url(r'^(.*?)/(.*?)/comments$', models_view.comments),
    url(r'^(.*?)/(.*?)/insights$', models_view.insights),
    url(r'^(.*?)/(.*?)/settings$', models_view.settings),
    url(r'^upload$', models_view.upload_modelfile, name='upload_modelfile'),
    url(r'^download$', models_view.download_model, name='download_model'),
    url(r'^(.*?)/new', models_view.new_model, name='new_model'),
    url(r'^(.*?)/(.*?)/settings/delete$', models_view.drop_model, name='drop_model'),

    # Comments #
    url(r'^(.*?)/(.*?)/comments/new$', models_view.new_comment),
    url(r'^(.*?)/(.*?)/comments/delete$', models_view.delete_comment),
]


