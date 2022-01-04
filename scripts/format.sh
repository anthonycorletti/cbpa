#!/bin/sh -ex

# Sort imports one per line, so autoflake can remove unused imports
isort --force-single-line-imports coinbasepro_scheduler tests scripts

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place coinbasepro_scheduler tests scripts --exclude=__init__.py
black coinbasepro_scheduler tests scripts
isort coinbasepro_scheduler tests scripts
