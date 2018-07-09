"""
Definition of urls for UserProfile.
"""

from UserProfile import views as profile_view
from django.conf.urls import include, url

urlpatterns = [
    # Models Pages #
    url(r'^$', profile_view.user_profile, name='user-profile'),
]



