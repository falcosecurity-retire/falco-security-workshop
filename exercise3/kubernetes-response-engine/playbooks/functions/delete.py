import playbooks
from playbooks import infrastructure


subscriber = playbooks.AlertSubscriber.create_from_environment_variables(
    playbooks.DeletePod(infrastructure.KubernetesClient())
)


def handler(event, context):
    subscriber.receive(event)
