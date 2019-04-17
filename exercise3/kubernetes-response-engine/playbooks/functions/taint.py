import os
import playbooks
from playbooks import infrastructure


subscriber = playbooks.AlertSubscriber.create_from_environment_variables(
    playbooks.TaintNode(
        infrastructure.KubernetesClient(),
        os.environ.get('TAINT_KEY', 'falco/alert'),
        os.environ.get('TAINT_VALUE', 'true'),
        os.environ.get('TAINT_EFFECT', 'NoSchedule')
    )
)


def handler(event, context):
    subscriber.receive(event)
