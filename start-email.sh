#!/bin/sh

# Email application development env shell script
# TODO: Email container can't be started by docker-compose's up command 
docker-compose -f docker-compose-dev.yml up email
