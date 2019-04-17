import os
import playbooks
from playbooks import infrastructure


def _to_bool(value):
    return value.lower() in ('yes', 'true', '1')


subscriber = playbooks.AlertSubscriber.create_from_environment_variables(
    playbooks.CreateIncidentInDemisto(
        infrastructure.DemistoClient(os.environ['DEMISTO_API_KEY'],
                                     os.environ['DEMISTO_BASE_URL'],
                                     verify_ssl=_to_bool(
                                         os.environ.get('VERIFY_SSL', 'True'))
                                     )
    )
)


def handler(event, context):
    subscriber.receive(event)
