#!/bin/bash

export MINIKUBE_WANTUPDATENOTIFICATION=false
export MINIKUBE_WANTREPORTERRORPROMPT=false
export MINIKUBE_HOME=$HOME
export CHANGE_MINIKUBE_NONE_USER=true
export KUBECONFIG=$HOME/.kube/config
mkdir -p $HOME/.kube $HOME/.minikube
touch $KUBECONFIG

sudo -E minikube start --vm-driver none

sudo chown -R falco:falco ~falco/.minikube

kubectl apply -f k8s-using-daemonset/k8s-with-rbac/falco-service.yaml 



sudo mkdir -p /var/lib/k8s_audit

cd k8s_audit_config
FALCO_SERVICE_CLUSTERIP=$(kubectl get service falco-service -o=jsonpath={.spec.clusterIP}) envsubst < webhook-config.yaml.in > webhook-config.yaml
sudo cp audit-policy.yaml /var/lib/k8s_audit
sudo cp webhook-config.yaml /var/lib/k8s_audit
sudo cp apiserver-config.patch.sh /var/lib/k8s_audit
sudo bash /var/lib/k8s_audit/apiserver-config.patch.sh /etc/kubernetes/manifests/kube-apiserver.yaml minikube
cd -
