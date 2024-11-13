# pylint: disable=no-name-in-module, line-too-long

import sys

from .views import external_moderation_request, external_moderation_requests

if sys.version_info[0] > 2:
    from django.urls import re_path

    urlpatterns = [
        re_path(r'^requests$', external_moderation_requests, name='external_moderation_requests'),
        re_path(r'^(?P<request_id>.+)/moderate$', external_moderation_request, name='external_moderation_request'),
    ]
else:
    from django.conf.urls import url

    urlpatterns = [
        url(r'^requests$', external_moderation_requests, name='external_moderation_requests'),
        url(r'^(?P<request_id>.+)/moderate$', external_moderation_request, name='external_moderation_request'),
    ]
