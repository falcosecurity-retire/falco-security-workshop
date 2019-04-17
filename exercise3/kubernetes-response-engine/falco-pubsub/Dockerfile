FROM golang:1.12 as builder
WORKDIR /falco-pubsub
COPY go.mod go.sum ./
COPY *.go ./
RUN GOOS=linux GOARCH=amd64 CGO_ENABLED=0 go build -ldflags="-s" -o falco-pubsub main.go
RUN strip falco-pubsub


FROM alpine
RUN apk add --no-cache ca-certificates
COPY --from=builder /falco-pubsub/falco-pubsub /bin/falco-pubsub
CMD ["/bin/falco-pubsub"]
