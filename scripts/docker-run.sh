#!/bin/sh -e

docker run -d cbps python coinbasepro_scheduler/main.py -f ${@}
