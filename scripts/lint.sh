#!/bin/sh -ex

mypy coinbasepro_scheduler
flake8 coinbasepro_scheduler tests
black coinbasepro_scheduler tests --check
isort coinbasepro_scheduler tests scripts --check-only
