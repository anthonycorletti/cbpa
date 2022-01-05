#!/bin/sh -ex

# Sort imports one per line, so autoflake can remove unused imports
isort --force-single-line-imports cbpa tests scripts

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place cbpa tests scripts --exclude=__init__.py
black cbpa tests scripts
isort cbpa tests scripts
