"""
Definition of urls for Models.
"""

from Models import views as models_view
from django.conf.urls import include, url

urlpatterns = [
    # Download & Upload #
    url(r'(.*?)/(.*?)/upload$', models_view.upload_modelfile, name='upload-modelfile'),
    url(r'(.*?)/(.*?)/download$', models_view.download_model, name='download-model'),
    
    # Model Settings #
    url(r'(.*?)/create$', models_view.create_model, name='create_model'),
    url(r'(.*?)/(.*?)/settings/delete$', models_view.drop_model, name='drop-model'),
    url(r'(.*?)/(.*?)/settings$', models_view.settings),
    
    # Stars #
    url(r'(.*?)/(.*?)/star$', models_view.star, name='star'),
    url(r'(.*?)/(.*?)/unstar$', models_view.unstar, name='unstar'),

    # Model Insights #
    url(r'(.*?)/(.*?)/insights$', models_view.insights),

    # Model Profile #
    url(r'(.*?)/(.*?)/$', models_view.models, name='models'),
    
    # Modelfiles #
    url(r'(.*?)/(.*?)/(.*?)/$', models_view.modelfile),

    # Comments #
    url(r'(.*?)/(.*?)/comments/new$', models_view.new_comment, name='new-comment'),
    url(r'(.*?)/(.*?)/comments/delete$', models_view.delete_comment, name='delete-comment'),
    url(r'(.*?)/(.*?)/comments$', models_view.comments),
    
    # Model Ranking List #
    url(r'^culling$', models_view.culling, name='culling'),

]


