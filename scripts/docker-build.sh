#!/bin/sh -e

docker build -t gcr.io/$(gcloud config list --format 'value(core.project)')/cbpa .
