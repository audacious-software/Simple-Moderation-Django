# pylint: disable=no-member, line-too-long
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.cache import never_cache


from .models import ExternalModerationRequest

@never_cache
@login_required
def external_moderation_request(request, request_id): # pylint: disable=unused-argument
    moderation_request = get_object_or_404(ExternalModerationRequest, pk=int(request_id))

    context = {
        'moderation_request': moderation_request
    }

    if request.method == 'POST':
        action = request.POST.get('action', None)

        response =  request.POST.get('response', None)

        if action is None:
            payload = {
                'success': False,
                'error': '"action" parameter missing.'
            }

            return HttpResponse(json.dumps(payload, indent=2), content_type='application/json', status=500)

        moderation_request.response = response
        moderation_request.moderator = request.user

        if action == 'approve':
            moderation_request.approved = timezone.now()
        elif action == 'deny':
            moderation_request.denied = timezone.now()
        else:
            payload = {
                'success': False,
                'error': 'Unknown "action": %s' % action
            }

            return HttpResponse(json.dumps(payload, indent=2), content_type='application/json', status=500)

        moderation_request.save()

        payload = {
            'success': True
        }

        return HttpResponse(json.dumps(payload, indent=2), content_type='application/json', status=201)

    return render(request, 'external_moderation_request.html', context=context)

@never_cache
@login_required
def external_moderation_requests(request): # pylint: disable=too-many-locals, too-many-branches, too-many-statements
    context = {}

    search_query = request.GET.get('query', '').lower()

    query = ExternalModerationRequest.objects.all()

    state = request.GET.get('state', '')

    if state != '':
        # requested = models.DateTimeField()
        # approved = models.DateTimeField(null=True, blank=True)
        # denied = models.DateTimeField(null=True, blank=True)

        # query = query.filter(study_arm__identifier=state)

        pass

    context['state'] = state

    context['search_query'] = search_query

    context['requests'] = list(query)

    if search_query != '':
        new_requests = []

        for moderation_request in context['requests']:
            if moderation_request.message is not None and search_query in moderation_request.message.lower():
                new_requests.append(moderation_request)
            elif moderation_request.response is not None and search_query in moderation_request.response.lower():
                new_requests.append(moderation_request)

        context['requests'] = new_requests

    context['total'] = len(context['requests'])

    page = int(request.GET.get('page', '0'))
    page_size = int(request.GET.get('size', '25'))

    start_item = page_size * page

    if page_size != -1:
        context['requests'] = context['requests'][start_item:(start_item+page_size)]

    context['current_page'] = page
    context['pages'] = context['total'] / page_size
    context['size'] = page_size

    context['end_item'] = start_item + page_size

    if page_size == -1:
        context['current_page'] = 0
        context['pages'] = 1

        start_item = 0
        context['end_item'] = context['total']

    if context['end_item'] > context['total']:
        context['end_item'] = context['total']

    context['start_item'] = start_item + 1

    base_url = reverse('external_moderation_requests')

    if page > 0:
        context['previous_page'] = '%s?page=%s&size=%s' % (base_url, page - 1, page_size)

    if context['total'] > (page + 1) * page_size:
        context['next_page'] = '%s?page=%s&size=%s' % (base_url, page + 1, page_size)

    context['first_page'] = '%s?page=%s&size=%s' % (base_url, 0, page_size)

    context['last_page'] = '%s?page=%s&size=%s' % (base_url, context['total'] / page_size, page_size)

    if page_size == -1:
        context['last_page'] = '%s?page=%s&size=%s' % (base_url, 0, page_size)
        del context['next_page']

    if (context['total'] % page_size) != 0:
        context['pages'] += 1

    context['states'] = (
        ('unmoderated', 'Unmoderated',),
        ('approved', 'Approved',),
        ('denied', 'Denied',),
        ('timed_out', 'Timed Out',),
    )

    return render(request, 'external_moderation_requests.html', context=context)
