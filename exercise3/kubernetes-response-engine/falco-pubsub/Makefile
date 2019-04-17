build:
	GOOS=linux GOARCH=amd64 CGO_ENABLED=0 go build -ldflags="-s" -o falco-pubsub main.go

clean:
	rm falco-pubsub

docker: build
	docker build -t sysdiglabs/falco-pubsub .
	docker push sysdiglabs/falco-pubsub
