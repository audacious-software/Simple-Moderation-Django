# pylint: disable=line-too-long

import json

from django.utils import timezone

from django_dialog_engine.dialog import BaseNode, DialogTransition

from django_dialog_engine_moderation.models import ExternalModerationRequest

class ExternalModerationBranch(BaseNode):
    @staticmethod
    def parse(dialog_def):
        if dialog_def['type'] == 'external-moderation':
            try:
                moderation_node = ExternalModerationBranch(dialog_def['id'], dialog_def['approve_action'], dialog_def['deny_action'], dialog_def.get('timeout_action', None), dialog_def.get('timeout_interval', None), dialog_def['message'], dialog_def.get('response_variable', None))

                return moderation_node
            except KeyError:
                pass

        return None

    def __init__(self, node_id, approve_action, deny_action, timeout_action, timeout_interval, message, response_variable): # pylint: disable=too-many-arguments
        super(ExternalModerationBranch, self).__init__(node_id, node_id) # pylint: disable=super-with-arguments

        self.approve_action = approve_action
        self.deny_action = deny_action
        self.timeout_action = timeout_action
        self.timeout_interval = timeout_interval
        self.message = message
        self.response_variable = response_variable

    def node_type(self):
        return 'external-moderation'

    def str(self):
        definition = {
            'id': self.node_id,
            'approve_action': self.approve_action,
            'deny_action': self.deny_action,
            'message': self.message,
        }

        if self.timeout_action is None:
            definition['timeout_action'] = self.timeout_action

        if self.timeout_interval is None:
            definition['timeout_interval'] = self.timeout_interval

        if self.response_variable is None:
            definition['response_variable'] = self.response_variable

        return json.dumps(definition, indent=2)

    def evaluate(self, dialog, response=None, last_transition=None, extras=None, logger=None): # pylint: disable=too-many-arguments, too-many-locals, too-many-branches, too-many-statements
        requester_id = '%s:%s' % (last_transition.dialog.pk, self.node_id)

        pending = ExternalModerationRequest.objects.fetch_latest_pending_request(requester_id)

        if pending is None:
            ExternalModerationRequest.objects.create_moderation_request(requester_id, self.message)

            return None

        if pending.approved is not None:
            transition = DialogTransition(new_state_id=self.approve_action)

            transition.metadata['reason'] = 'moderation-approved'
            transition.metadata['approved_date'] = pending.approved.isoformat()

            if self.response_variable is not None:
                transition.metadata['exit_actions'] = [{
                    'type': 'store-value',
                    'key': self.response_variable,
                    'value': pending.response
                }]

            pending.used = timezone.now()
            pending.save()

            return transition

        if pending.denied is not None:
            transition = DialogTransition(new_state_id=self.deny_action)

            transition.metadata['reason'] = 'moderation-approved'
            transition.metadata['denied_date'] = pending.denied.isoformat()

            if self.response_variable is not None:
                transition.metadata['exit_actions'] = [{
                    'type': 'store-value',
                    'key': self.response_variable,
                    'value': pending.response
                }]

            pending.used = timezone.now()
            pending.save()

            return transition

        if self.timeout_action is not None and self.timeout_interval is not None:
            now = timezone.now()

            if (now - last_transition.when).total_seconds() > self.timeout_interval:
                transition = DialogTransition(new_state_id=self.timeout_action)

                transition.metadata['reason'] = 'moderation-timeout'
                transition.metadata['timeout_duration'] = self.timeout_interval

                pending.used = timezone.now()
                pending.save()

                return transition

        return None

    def actions(self):
        return []

    def next_nodes(self):
        nodes = [
            self.approve_action,
            self.deny_action,
        ]

        if self.timeout_action is not None:
            nodes.append(self.timeout_action)

        return nodes

def dialog_builder_cards():
    return [
        ('External Moderation', 'external-moderation',),
    ]
