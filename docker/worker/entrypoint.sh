#!/bin/sh

/code/docker/wait-for-it.sh redis:6379
exec "$@"
