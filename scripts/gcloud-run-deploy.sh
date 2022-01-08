#!/bin/sh -ex

PROJECT_ID=$(gcloud config list --format 'value(core.project)')
VERSION=${VERSION:=latest}
IMAGE=gcr.io/${PROJECT_ID}/cbpa:${VERSION}
SECRET_ID=${SECRET_ID}
gcloud beta run deploy cbpa --no-allow-unauthenticated --quiet --image=$IMAGE --update-env-vars PROJECT_ID=${PROJECT_ID},SECRET_ID=${SECRET_ID}
