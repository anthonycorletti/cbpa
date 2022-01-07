#!/bin/sh -ex

PROJECT_ID=$(gcloud config list --format 'value(core.project)')
VERSION=${VERSION:=latest}
IMAGE=gcr.io/${PROJECT_ID}/cbpa:${VERSION}
gcloud beta run deploy cbpa --no-allow-unauthenticated --quiet --image=$IMAGE
