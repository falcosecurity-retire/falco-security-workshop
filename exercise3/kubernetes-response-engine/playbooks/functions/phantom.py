import os
import playbooks
from playbooks import infrastructure


def _to_bool(value):
    return value.lower() in ('yes', 'true', '1')


subscriber = playbooks.AlertSubscriber.create_from_environment_variables(
    playbooks.CreateContainerInPhantom(
        infrastructure.PhantomClient(
            os.environ['PHANTOM_USER'],
            os.environ['PHANTOM_PASSWORD'],
            os.environ['PHANTOM_BASE_URL'],
            verify_ssl=_to_bool(
                os.environ.get('VERIFY_SSL', 'True')
            )
        )
    )
)


def handler(event, context):
    subscriber.receive(event)
