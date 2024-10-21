#!/bin/bash -e

GHOST_CONTENT_PATH=${GHOST_CONTENT_PATH:-/home/deploy/ghost/ghost-data/content}
echo creating volume $GHOST_CONTENT_PATH
docker volume create --driver local \
  --opt type=ext4 \
  --opt o=bind \
  --opt device=$GHOST_CONTENT_PATH \
  ghost_volume

GHOST_ENDPOINT=${GHOST_ENDPOINT:-https://dlennon.org/posts/}
echo creating container: $GHOST_ENDPOINT
docker image build \
  --build-arg ENDPOINT=$GHOST_ENDPOINT \
  -t ghost_image .

# To keep systemd happy, run this in the background instead of daemonizing.  This ensures that
# the PID and PPID are as systemd expects when it does its fork and exec.
docker run \
  --name docker.ghost.service \
  -p 2368:2368 \
  --mount type=volume,source=ghost_volume,target=/home/ghost/server/content \
  ghost_image &

# Capure the PID
PID=$!
echo $PID > /home/deploy/ghost/ghost-stack/ghost.pid

# Wait until we can successfully hit the endpoint.  Again, this is for systemd, because it blocks
# only until the process that launches the daemon (i.e., this script) terminates.
until curl --output /dev/null --silent --head --fail http://localhost:2368/posts; do
  sleep 1
done
