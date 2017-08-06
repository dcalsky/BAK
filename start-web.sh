#!/bin/sh

# Web application development env shell script
docker-compose -f docker-compose-dev.yml run --rm --service-ports  web
