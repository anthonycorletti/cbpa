#!/bin/sh -ex

mypy cbpa
flake8 cbpa tests
black cbpa tests --check
isort cbpa tests scripts --check-only
