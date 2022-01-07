#!/bin/sh -e

PROJECT_ID=$(gcloud config list --format 'value(core.project)')
VERSION=${VERSION:=latest}
docker run -it gcr.io/${PROJECT_ID}/cbpa:${VERSION} /bin/sh
