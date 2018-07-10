"""
Definition of urls for Models.
"""

from Models import views as models_view
from django.conf.urls import include, url

urlpatterns = [
    # Model Ranking List #
    url(r'^culling$', models_view.culling, name='culling'),

    # Download & Upload #
    url(r'^(.*?)/(.*?)/upload$', models_view.upload_modelfile, name='upload_modelfile'),
    url(r'^(.*?)/(.*?)/download$', models_view.download_model, name='download_model'),
    
    # Model Settings #
    url(r'^(.*?)/new', models_view.new_model, name='new_model'),
    url(r'^(.*?)/(.*?)/settings/delete$', models_view.drop_model, name='drop_model'),
    url(r'^(.*?)/(.*?)/settings$', models_view.settings),
    
    # Stars #
    url(r'^(.*?)/(.*?)/star$', models_view.star, name='star'),
    url(r'^(.*?)/(.*?)/unstar$', models_view.unstar, name='unstar'),

    # Comments #
    url(r'^(.*?)/(.*?)/comments$', models_view.comments),
    url(r'^(.*?)/(.*?)/comments/new$', models_view.new_comment),
    url(r'^(.*?)/(.*?)/comments/delete$', models_view.delete_comment),

    # Model Insights #
    url(r'^(.*?)/(.*?)/insights$', models_view.insights),

    # Model Profile #
    url(r'^(.*?)/(.*?)/$', models_view.models, name='models'),
    
    # Modelfiles #
    url(r'^(.*?)/(.*?)/(.*?)$', models_view.modelfile),
]


