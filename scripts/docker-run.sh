#!/bin/sh -e

docker run -it gcr.io/$(gcloud config list --format 'value(core.project)')/cbpa ${@}
