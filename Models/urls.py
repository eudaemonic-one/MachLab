"""
Definition of urls for Models.
"""

from Models import views as models_view
from django.conf.urls import include, url

urlpatterns = [
    # Download & Upload #
    url(r'(.*?)/(.*?)/upload$', models_view.modelfile_upload, name='upload-modelfile'),
    url(r'(.*?)/(.*?)/download$', models_view.model_download, name='download-model'),
    
    # Model Settings #
    url(r'(.*?)/(.*?)/settings/delete$', models_view.model_delete, name='drop-model'),
    url(r'(.*?)/(.*?)/settings$', models_view.settings),
    
    # Stars #
    url(r'(.*?)/(.*?)/star$', models_view.star, name='star'),
    url(r'(.*?)/(.*?)/unstar$', models_view.unstar, name='unstar'),

    # Model Insights #
    url(r'(.*?)/(.*?)/insights$', models_view.insights),
    url(r'(.*?)/(.*?)/insights/(.*?)$', models_view.insights_display),

    # Modelfiles #
    url(r'(.*?)/(.*?)/(.*?)/$', models_view.modelfile),
    url(r'(.*?)/(.*?)/(.*?)/delete$', models_view.modelfile_delete),
    
    # Model Profile #
    url(r'(.*?)/(.*?)/$', models_view.models, name='models'),
    
    # Comments #
    url(r'(.*?)/(.*?)/comments/new$', models_view.comment_new, name='new-comment'),
    url(r'(.*?)/(.*?)/comments/delete$', models_view.comment_delete, name='delete-comment'),
    url(r'(.*?)/(.*?)/comments$', models_view.comments),
    
    # Model Create #
    url(r'(.*?)/create$', models_view.model_create, name='create_model'),

    # Model Ranking List #
    url(r'^ranking-list', models_view.ranking_list, name='ranking-list'),

]


