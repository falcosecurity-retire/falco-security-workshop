from mamba import description, it, context, before
from doublex import Spy
from doublex_expects import have_been_called_with, have_been_called
from expects import expect, raise_error

import json
import base64
from playbooks import AlertSubscriber


class _FakePlaybook(object):
    def run(self, alert):
        pass


with description(AlertSubscriber) as self:
    with before.each:
        self.playbook = Spy(_FakePlaybook)

        self.alert = {'irrelevant alert key': 'irrelevant alert value'}
        self.message = {
            'attributes': {
                'rule': 'falco.warning.terminal_shell_in_container',
            },
            'data': self.alert
        }

    with it('is subscribed to all topics if alert does not contain attribute.rule key'):
        message = {'data': self.alert}

        subscriber = AlertSubscriber(
            self.playbook,
            channels=['falco.warning.terminal_shell_in_container']
        )

        subscriber.receive(message)

        expect(self.playbook.run).to(have_been_called_with(self.alert))

    with it('is subscribed to all topics if subscriber does not specify channels'):
        subscriber = AlertSubscriber(self.playbook)

        subscriber.receive(self.message)

        expect(self.playbook.run).to(have_been_called_with(self.alert))

    with context('when is subscribed to channel'):
        with it('passes the alert to the playbook'):
            subscriber = AlertSubscriber(
                self.playbook,
                channels=['falco.warning.terminal_shell_in_container']
            )

            subscriber.receive(self.message)

            expect(self.playbook.run).to(have_been_called_with(self.alert))

    with context('when is subscribed to channel'):
        with it('does not pass the alert to the playbook'):
            subscriber = AlertSubscriber(
                self.playbook,
                channels=['falco.error.write_on_bin_directory']
            )

            subscriber.receive(self.message)

            expect(self.playbook.run).not_to(have_been_called)

    with it('parses alert sent to a NATS topic'):
        alert = {
            'irrelevant alert key for NATS':
            'irrelevant alert value for NATS'
        }
        nats_message = {
            'data': alert
        }
        subscriber = AlertSubscriber(
            self.playbook,
        )

        subscriber.receive(nats_message)

        expect(self.playbook.run).to(have_been_called_with(alert))

    with it('parses alert sent to a SNS Queue'):
        alert = {'irrelevant key for SNS': 'irrelevant value for SNS'}
        sns_message = {
            'Records': [{
                'Sns': {
                    'Message': json.dumps(alert)
                }
            }]
        }
        subscriber = AlertSubscriber(
            self.playbook,
        )

        subscriber.receive(sns_message)

        expect(self.playbook.run).to(have_been_called_with(alert))

    with it('parses alert sent to a Google PubSub topic'):
        alert = {'irrelevant key for PubSub': 'irrelevant value for PubSub'}
        pubsub_message = {
            'data': base64.b64encode(str.encode(json.dumps(alert)))
        }
        subscriber = AlertSubscriber(
            self.playbook,
        )

        subscriber.receive(pubsub_message)

        expect(self.playbook.run).to(have_been_called_with(alert))

    with context('when alert cannot be parsed'):
        with it("raises an error and doesn't send message to playbook"):
            message = {}
            subscriber = AlertSubscriber(
                self.playbook,
            )

            expect(lambda: subscriber.receive(message))\
                .to(raise_error(ValueError, "falco alert couldn't be parsed"))

            expect(self.playbook.run).not_to(have_been_called)
