
Docker volume
====

[driver specific options](https://docs.docker.com/reference/cli/docker/volume/create/#opt)

```bash

# create volume (bind is useful for development)
docker volume create --driver local \
  --opt type=ext4 \
  --opt o=bind \
  --opt device=/home/dnlennon/Workspace/repos/ghost-data/content \
  ghost_volume

# remove volume
docker volume rm content

```

Docker image and container
====

```bash
export CONTAINER_USERNAME=node

# (re)build the docker image
docker image build \
  --build-arg username=$CONTAINER_USERNAME \
  -t ghost_container .

# create a container
docker run --rm -d \
  --name ghost_container \
  -p 2368:2368 \
  --mount type=volume,source=ghost_volume,target=/home/$CONTAINER_USERNAME/server/content \
  ghost

# inspect the container
docker exec -i -t ghost_container /bin/sh --login 

# stop the container 
docker stop -t 0 ghost_container
```

