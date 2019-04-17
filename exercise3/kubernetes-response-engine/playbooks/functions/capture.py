import os
import playbooks
from playbooks import infrastructure


capture_duration = int(os.environ.get('CAPTURE_DURATION', 120)),

if "AWS_S3_BUCKET" in os.environ and "AWS_ACCESS_KEY_ID" in os.environ and "AWS_SECRET_ACCESS_KEY" in os.environ:
    playbook = playbooks.StartSysdigCaptureForContainerS3(
        infrastructure.KubernetesClient(),
        capture_duration,
        os.environ['AWS_S3_BUCKET'],
        os.environ['AWS_ACCESS_KEY_ID'],
        os.environ['AWS_SECRET_ACCESS_KEY']
    )

if "GCLOUD_BUCKET" in os.environ:
    playbook = playbooks.StartSysdigCaptureForContainerGcloud(
        infrastructure.KubernetesClient(),
        capture_duration,
        os.environ['GCLOUD_BUCKET']
    )


subscriber = playbooks.AlertSubscriber.create_from_environment_variables(
    playbook
)


def handler(event, context):
    subscriber.receive(event)
