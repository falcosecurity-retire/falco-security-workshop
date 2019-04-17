import os
import playbooks
from playbooks import infrastructure


subscriber = playbooks.AlertSubscriber.create_from_environment_variables(
    playbooks.AddMessageToSlack(
        infrastructure.SlackClient(os.environ['SLACK_WEBHOOK_URL'])
    )
)


def handler(event, context):
    subscriber.receive(event)
