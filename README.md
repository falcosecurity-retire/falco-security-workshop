# Container Security Workshop with Falco

This repository contains the necessary files required to go through the exercises in the [Container Security Workshop](https://setns.run/falcows) offered by the [Falco](https://falco.org/) team. Typically this workshop is offered as an instructor led course.

## Exercises

Container Security Workshop - [Google Slides](https://setns.run/falcows)

Each exercise contains a `commands` file with the commands to complete the exercise. In addition, the [slides](https://setns.run/falcows) contain the commands to run and the expected output. 

### Exercise 1

This exercise walks you through the Falco basics. It teaches you about Falco rules, and how to use [Sysdig](https://github.com/draios/sysdig) to profile an application to create custom rules. At the end of this exercise, you'll understand how to write your own Falco rules.

### Exercise 2

This exercise walks you through deploying Falco on Kubernetes and how to integrate Falco with [Kubernetes Audit Logging](https://kubernetes.io/docs/tasks/debug-application-cluster/audit/). At the end of this exercise you'll understand how Kubernetes audit logging works and how Falco can detect abnormal behavior through Kubernetes audit logs.

### Exercise 3

This exercise walks you through implementing a [Response Engine with Security Playbooks](https://github.com/falcosecurity/kubernetes-response-engine). The playbooks are implemented as Serverless functions and allow you to take action based on Falco alerts. As part of this, you'll deploy Falco via [Helm](https://helm.sh/), as well as deploy [NATS](https://nats.io/) and [Kubeless](https://kubeless.io/). At the end of this exercise, you'll understand how to take automated action on Falco alerts.

### Exercise 4

This exercise walks you through setting up an EFK ([Elasticsearch](https://www.elastic.co/products/elasticsearch), [Fluentd](https://www.fluentd.org/), and [Kibana](https://www.elastic.co/products/kibana)) stack and collecting Falco alerts for storage and analysis. You'll deploy Falco and the EFK stack via Helm, and create visualizations and dashboards in Kibana. At the end of the exercise, you'll understand how to collect and store Falco alerts, as well as how to visualize the alerts.

## Required Workstation

### AWS

For simplicity we've provided an AWS AMI (ami-0893c0781761fa458, us-east-1) that provides a workstation with all the required software. 

* Setup Script: `/usr/local/bin/setup-falco.sh` 
    * This script *MUST* be ran by the `falco` user after the first login (or as part of the instance's userdata). This script clones the latest version of the training (this repo), installs the latest version of Sysdig, and configures other tools required. If running the script manually, it is suggested to logout and back in after running the script.   
* Suggested Instance Type: m4.large (2 cpu, 8 GB RAM minimum)
* User: falco
* Pass: FalcoCSWS! (must be changed at first login)
* Required Ports: 22, 8000 (only for exercise 4)

### Roll Your Own

If you wish to build your own workstation image, you can reference the Packer template provided in [this repo](https://github.com/draios/sysdig-workshop-infra/blob/master/packer/ubuntu-1604-falco.json). Anything installed in the image is done primarily by a [Chef Cookbook](https://github.com/draios/sysdig-workshop-infra/tree/master/cookbooks/falco_workstation). Additional software is installed by the `setup-falco.sh` script in order to pull the latest versions.  

## License

![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/80x15.png) This work is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).

**You are free to:**
* **Share** — copy and redistribute the material in any medium or format
* **Adapt** — remix, transform, and build upon the material
for any purpose, even commercially.

**Under the following terms:**
* **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.

* **ShareAlike** — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.

* **No additional restrictions** — You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.

For the full text of the license, see [COPYING](./COPYING).

