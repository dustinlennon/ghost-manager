#!/bin/bash
rm -f /home/deploy/ghost/ghost-manager/ghost.pid
docker stop -t 0 docker.ghost.service || true
docker rm docker.ghost.service || true
docker volume rm ghost_volume || true
