# pylint: disable=no-member, line-too-long
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import importlib
import json

from django.conf import settings
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

    message = models.TextField(max_length=(1024 * 1024)) # pylint: disable=superfluous-parens

    response = models.TextField(max_length=(1024 * 1024), null=True, blank=True) # pylint: disable=superfluous-parens

    automatic_decision = models.BooleanField(default=False)

    requester_id = models.CharField(max_length=1024, default='unknown-requester')

    def get_absolute_url(self):
        return reverse('external_moderation_request', args=[self.pk])

    def moderate(self):
        for app in settings.INSTALLED_APPS:
            try:
                moderation_api = importlib.import_module(app + '.moderation_api')

                for moderator in Moderator.objects.filter(active=True):
                    approved, metadata = moderation_api.moderate(self, moderator)

                    if approved is not None:
                        ModerationDecision.objects.create(request=self, approved=approved, decision_maker=moderator.moderator_id, metadata=metadata, when=timezone.now())
            except ImportError:
                pass
            except AttributeError:
                pass

    def resolve(self): # pylint: disable=too-many-return-statements, too-many-branches
        if (self.approved is not None) or (self.denied is not None) or (self.timed_out is not None):
            return True

        automated_votes = 0.0
        approve_votes = 0.0
        deny_votes = 0.0

        for moderator in Moderator.objects.filter(active=True):
            decision = ModerationDecision.objects.filter(decision_maker=moderator.moderator_id, request=self).order_by('-when').first()

            if decision is not None:
                if decision.approved:
                    approve_votes += 1

                    if decision.decision_maker.startswith('user:'): # If a human approves, override over other votes.
                        metadata = json.loads(decision.metadata)

                        self.approved = timezone.now()

                        response = metadata.get('response', None)

                        if response is not None:
                            self.response = response

                        self.save()

                        return True

                    automated_votes += 1
                else:
                    deny_votes += 1

                    if decision.decision_maker.startswith('user:'): # If a human approves, override over other votes.
                        metadata = json.loads(decision.metadata)

                        self.denied = timezone.now()

                        response = metadata.get('response', None)

                        if response is not None:
                            self.response = response

                        self.save()

                        return True

                    automated_votes += 1

        if automated_votes == 0:
            return False

        if (deny_votes / automated_votes) >= settings.SIMPLE_MODERATION_AUTOMATED_DENIAL_THRESHOLD:
            self.denied = timezone.now()
            self.automatic_decision = True
            self.save()

            return True

        if (approve_votes / automated_votes) >= settings.SIMPLE_MODERATION_AUTOMATED_APPROVAL_THRESHOLD:
            self.approved = timezone.now()
            self.automatic_decision = True
            self.save()

            return True

        return False

class ModerationDecision(models.Model):
    request = models.ForeignKey(ExternalModerationRequest, related_name='decisions', on_delete=models.CASCADE)

    approved = models.BooleanField(default=True)
    decision_maker = models.CharField(max_length=1024)
    when = models.DateTimeField()

    metadata = models.TextField(max_length=(4 * 1024 * 1024), null=True, blank=True)

class Moderator(models.Model):
    moderator_id = models.CharField(max_length=1024, unique=True)

    moderator_for = models.TextField(max_length=(4 * 1024 * 1024), default='*')

    active = models.BooleanField(default=True)

    metadata = models.JSONField(max_length=(4 * 1024 * 1024), default=dict, blank=True)
