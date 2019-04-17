import os
import re
import fnmatch
import json
import base64


class AlertSubscriber(object):
    def __init__(self, playbook, channels=[]):
        self._channels = channels
        self._playbook = playbook

        self._channels_as_regexp = [
            re.compile(fnmatch.translate(channel.strip()))
            for channel in self._channels
        ]

    def receive(self, message):
        if self._handles_alert(message):
            alert = self._parse_alert_from(message)
            self._playbook.run(alert)

    def _handles_alert(self, message):
        if not(self._channels):
            return True

        if 'attributes' in message and 'rule' in message['attributes']:
            rule = message['attributes']['rule']
            if not self._matches_any_rule(rule):
                return False
        return True

    def _matches_any_rule(self, rule):
        return any(regexp.fullmatch(rule) for regexp in self._channels_as_regexp)

    def _parse_alert_from(self, message):
        # TODO: Use a parsing strategy instead of appending if/else stuff
        # There are 3 identified right now (three strikes and refactor,
        # remember?):
        # * NATS
        # * AWS SNS
        # * Google Pub/Sub

        if 'data' in message:
            data = message['data']

            # Google PubSub case
            if self._is_base64_encoded(data):
                return json.loads(base64.b64decode(data))

            # NATS case
            return data

        # SNS case
        if 'Records' in message:
            return json.loads(message['Records'][0]['Sns']['Message'])

        raise ValueError("falco alert couldn't be parsed")

    def _is_base64_encoded(self, value):
        try:
            base64.b64decode(value)
            return True
        except Exception:
            return False

    @classmethod
    def create_from_environment_variables(class_, playbook):
        return class_(
            playbook,
            channels=os.environ.get('SUBSCRIBED_ALERTS', '').split(',')
        )
