deploy: deploy_nats
	kubectl apply -f kubeless/
	kubectl apply -f .

deploy_nats:
	kubectl apply -f nats/deployment-rbac.yaml
	sleep 30
	kubectl apply -f nats/nats-cluster.yaml

clean:
	kubectl delete -f kubeless/
	kubectl delete -f nats/
	kubectl delete -f .
