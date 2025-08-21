# pylint: disable=line-too-long, no-member, import-outside-toplevel

import json
import logging
import traceback

from nltk.sentiment.vader import SentimentIntensityAnalyzer

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone

from .models import ModerationDecision

def moderate(request, moderator):
    logger = logging.getLogger()

    logger.warning('simple_moderation.moderate: %s -- %s', request, moderator)

    try:
        context = {
            'site_name': settings.SIMPLE_MODERATION_SITE_NAME,
            'site_url': settings.SIMPLE_MODERATION_SITE_URL,
            'request': request,
        }

        if moderator.moderator_id.startswith('user:'):
            email_address = moderator.metadata.get('email', None)

            if email_address is None:
                user = get_user_model().objects.filter(username__iexact=moderator.moderator_id[5:])

                if (user is not None) and (user.email_address is not None):
                    email_address = user.email_address

            logger.warning('simple_moderation.moderate.email: %s -- %s -- %s', request, moderator, email_address)

            if email_address is not None:
                subject = render_to_string('simple_moderation/email/email_subject.txt', context)
                body  = render_to_string('simple_moderation/email/email_body.txt', context)

                send_mail(subject, body, settings.SIMPLE_MODERATION_FROM_ADDRESS, [email_address], fail_silently=False)

            try:
                from simple_messaging.models import OutgoingMessage

                sms_number = moderator.metadata.get('sms', None)

                logger.warning('simple_moderation.moderate.sms: %s -- %s -- %s', request, moderator, sms_number)

                if sms_number is not None:
                    message  = render_to_string('simple_moderation/sms/sms_notification.txt', context)

                    OutgoingMessage.objects.create(destination=sms_number, send_date=timezone.now(), message=message)
            except ImportError:
                # pass
                logger.error('OK: %s', traceback.format_exc())

        if moderator.moderator_id.startswith('nltk-vader:'):
            sentiment_analyzer = SentimentIntensityAnalyzer()

            polarity_scores = sentiment_analyzer.polarity_scores(request.message)

            logger.warning('simple_moderation.moderate.nltk-vader: %s -- %s -- %s', request, moderator, polarity_scores)

            decision = ModerationDecision(request=request, when=timezone.now())
            decision.decision_maker = moderator.moderator_id
            decision.metadata = json.dumps(polarity_scores, indent=2)

            positive_threshold = moderator.metadata.get('positive_threshold', 0.5)
            negative_threshold = moderator.metadata.get('negative_threshold', 0.5)

            if polarity_scores['neg'] > negative_threshold:
                decision.approved = False
                decision.save()

                return

            if polarity_scores['pos'] > positive_threshold:
                decision.approved = True
                decision.save()

                return

    except: # pylint: disable=bare-except
        logger.error('simple_moderation.moderate ERROR: %s', traceback.format_exc())

    return (None, None)
