# Container Security Workshop with Falco

This repository contains the necessary files required to go through the exercises in the [Container Security Workshop](https://setns.run/falcows) offered by the [Falco](https://falco.org/) team. Typically this workshop is offered as an instructor led course.

## Exercises

### Exercise 1

This exercise walks you through the Falco basics. It teaches you about Falco rules, and how to use [Sysdig](https://github.com/draios/sysdig) to profile an application to create custom rules. At the end of this exercise, you'll understand how to write your own Falco rules.

### Exercise 2

This exercise walks you through deploying Falco on Kubernetes and how to integrate Falco with [Kubernetes Audit Logging](https://kubernetes.io/docs/tasks/debug-application-cluster/audit/). At the end of this exercise you'll understand how Kubernetes audit logging works and how Falco can detect abnormal behavior through Kubernetes audit logs.

### Exercise 3

This exercise walks you through implementing a [Response Engine with Security Playbooks](https://github.com/falcosecurity/kubernetes-response-engine). The playbooks are implemented as Serverless functions and allow you to take action based on Falco alerts. As part of this, you'll deploy Falco via [Helm](https://helm.sh/), as well as deploy [NATS](https://nats.io/) and [Kubeless](https://kubeless.io/). At the end of this exercise, you'll understand how to take automated action on Falco alerts.

### Exercise 4

This exercise wakls you through setting up an EFK ([Elasticsearch](https://www.elastic.co/products/elasticsearch), [Fluentd](https://www.fluentd.org/), and [Kibana](https://www.elastic.co/products/kibana)) stack and collecting Falco alerts for storage and analysis. You'll deploy Falco and the EFK stack via Helm, and create visualizations and dashboards in Kibana. At the end of the exercise, you'll understand how to collect and store Falco alerts, as well as how to visualize the alerts.

## Required Workstation

### AWS

For simplicity we've provided an AWS AMI (ami-045b9556899705148, us-east-1) that provides a workstation with all the required software. 

* Setup Script: `/usr/local/bin/setup-falco.sh` 
    * This script *MUST* be ran by the `falco` user after the first login (or as part of the instance's userdata). This script clones the latest version of the training (this repo), installs the latest version of Sysdig, and configures other tools required. If running the script manually, it is suggested to logout and back in after running the script.   
* Suggested Instance Type: m4.large (2 cpu, 8 GB RAM minimum)
* User: falco
* Pass: FalcoCSWS! (must be changed at first login)
* Required Ports: 22, 8000 (only for exercise 4)

### Roll Your Own

If you wish to build your own workstation image, you can reference the Packer template provided in [this repo](https://github.com/draios/sysdig-workshop-infra/blob/master/packer/ubuntu-1604-falco.json). Anything installed in the image is done primarily by a [Chef Cookbook](https://github.com/draios/sysdig-workshop-infra/tree/master/cookbooks/falco_workstation).
