// Copyright 2012-2019 The Sysdig Tech Marketing Team
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// +build ignore

package main

import (
	"bufio"
	"cloud.google.com/go/pubsub"
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"golang.org/x/oauth2/google"
	"google.golang.org/api/option"
	"log"
	"os"
	"regexp"
	"strconv"
	"strings"
	"sync"
	"time"
)

var (
	googleProjectID       = os.Getenv("GOOGLE_PROJECT_ID")
	googleCredentialsData = os.Getenv("GOOGLE_CREDENTIALS_DATA")
	slugRegularExpression = regexp.MustCompile("[^a-z0-9]+")
)

func main() {
	var pipePath = flag.String("f", "/var/run/falco/nats", "The named pipe path")
	var topicName = flag.String("t", "", "Topic to subscribe")

	if googleProjectID == "" || googleCredentialsData == "" {
		log.Fatalln("You need to provide the env vars GOOGLE_PROJECT_ID and GOOGLE_CREDENTIALS_DATA")
	}

	credentials, err := google.CredentialsFromJSON(context.Background(), []byte(googleCredentialsData), pubsub.ScopePubSub)
	if err != nil {
		log.Println("error creating the credentials object, trying again in case the credentials are double quoted...")
		googleCredentialsData, _ = strconv.Unquote(googleCredentialsData)
		credentials, err = google.CredentialsFromJSON(context.Background(), []byte(googleCredentialsData), pubsub.ScopePubSub)
		if err != nil {
			log.Fatalf("could not create credentials from json data: %v", err)
		}
	}

	log.SetFlags(0)
	flag.Usage = usage
	flag.Parse()

	if *topicName == "" {
		log.Fatalf("you must provide a topic name to subscribe using -t <topic_name>")
	}

	pubsubClient, err := pubsub.NewClient(context.Background(), googleProjectID, option.WithCredentials(credentials))
	if err != nil {
		log.Fatalf("could not create a new client for Google Project ID '%s': %v", googleProjectID, err)
	}
	defer pubsubClient.Close()

	log.Printf("Created new client for Google Project ID: %s", googleProjectID)

	pipe, err := os.OpenFile(*pipePath, os.O_RDONLY, 0600)
	if err != nil {
		log.Fatal(err)
	}
	log.Printf("Opened pipe %s", *pipePath)

	reader := bufio.NewReader(pipe)
	scanner := bufio.NewScanner(reader)
	log.Printf("Scanning %s", *pipePath)

	wg := &sync.WaitGroup{}

	for scanner.Scan() {
		msg := []byte(scanner.Text())
		wg.Add(1)
		go publish(pubsubClient, msg, *topicName, wg)
	}

	wg.Wait()

}

func publish(pubsubClient *pubsub.Client, msg []byte, topicName string, wg *sync.WaitGroup) {
	defer wg.Done()

	alert := parseAlert(msg)

	topic := pubsubClient.Topic(topicName)
	defer topic.Stop()

	message := &pubsub.Message{
		Data: msg,
		Attributes: map[string]string{
			"priority": alert.Priority,
			"rule":     alert.Rule,
		},
	}

	ctxPublish, cancelPublish := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancelPublish()

	result := topic.Publish(ctxPublish, message)

	ctxGet, cancelGet := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancelGet()

	id, err := result.Get(ctxGet)
	if err != nil {
		log.Printf("info: error publishing message: %v", err)
	} else {
		fmt.Printf("Published a message with a message ID: %s to topic %s\n", id, topicName)
	}
}

func usage() {
	log.Fatalf("Usage: %s [-s server] <subject> <msg> \n", os.Args[0])
}

type parsedAlert struct {
	Priority string `json:"priority"`
	Rule     string `json:"rule"`
}

func parseAlert(alert []byte) parsedAlert {
	var result parsedAlert
	err := json.Unmarshal(alert, &result)
	if err != nil {
		log.Fatal(err)
	}
	result.Rule = subjectAndRuleSlug(result)

	return result
}

func subjectAndRuleSlug(alert parsedAlert) (subject string) {

	subject = "falco." + alert.Priority + "." + slugify(alert.Rule)
	subject = strings.ToLower(subject)

	return subject
}

func slugify(input string) string {
	return strings.Trim(slugRegularExpression.ReplaceAllString(strings.ToLower(input), "_"), "_")
}
