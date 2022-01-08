#!/bin/sh -e

PROJECT_ID=$(gcloud config list --format 'value(core.project)')
VERSION=${VERSION:=latest}
docker run -it -p 8002:8002 gcr.io/${PROJECT_ID}/cbpa:${VERSION}
