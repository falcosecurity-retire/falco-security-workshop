# Terraform manifests for Kubernetes Response Engine running on GKE

In this directory you can find the Terraform manifests for creating a required
infrastructure for the Kubernetes Response Engine running with GKE technology:
Google Cloud Pub/Sub and Google Cloud Functions for executing the playbooks.

## Configuration

First of all you need to configure the variables needed for Google Cloud.
Open the file `terraform.tfvars` and edit it:

| Variable             | Contents                                                                                                                           |
|----------------------|------------------------------------------------------------------------------------------------------------------------------------|
| `gcloud_credentials` | Either the path to or the contents of a service account key file in JSON format. You can manage key files using the Cloud Console. |
| `gcloud_project`     | The default project to manage resources in.                                                                                        |
| `gcloud_zone`        | The default zone to manage resources in. Generally, this zone should be within the default region you specified.                   | 

## Deploy

For creating the resources, just run default Makefile target:

```
make
```

## Clean

You can clean everything with:

```
make clean
```
