#!/bin/sh -e

docker run -d cbps python cbpa/main.py -f ${@}
