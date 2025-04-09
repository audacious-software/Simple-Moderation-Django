# pylint: disable=no-member, line-too-long
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone

class ExternalModerationRequestManager(models.Manager):
    def create_moderation_request(self, requester_id, message):
        if requester_id is None:
            raise ValueError('Please provide a valid "requester_id" value.')

        if message is None:
            raise ValueError('Please provide a valid "message" value.')

        return self.create(requested=timezone.now(), message=message, requester_id=requester_id)

    def fetch_latest_pending_request(self, requester_id):
        if requester_id is None:
            raise ValueError('Please provide a valid "requester_id" value.')

        return self.filter(requester_id=requester_id, used=None).order_by('-requested').first()

class ExternalModerationRequest(models.Model):
    objects = ExternalModerationRequestManager()

    requested = models.DateTimeField()
    approved = models.DateTimeField(null=True, blank=True)
    denied = models.DateTimeField(null=True, blank=True)
    timed_out = models.DateTimeField(null=True, blank=True)

    used = models.DateTimeField(null=True, blank=True)

    message = models.TextField(max_length=(1024 * 1024))

    response = models.TextField(max_length=(1024 * 1024), null=True, blank=True)

    moderator = models.ForeignKey(get_user_model(), related_name='external_dialog_approvals', null=True, blank=True, on_delete=models.SET_NULL)

    requester_id = models.CharField(max_length=1024, default='unknown-requester')

    def get_absolute_url(self):
        return reverse('external_moderation_request', args=[self.pk])
