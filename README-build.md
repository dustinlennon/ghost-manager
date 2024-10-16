
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

```

Docker image and container
====

### build the image

```bash
# (re)build the docker image
docker image build \
  -t ghost_image .
```


### create a container
```bash
# create a container
docker run --rm -d \
  --name ghost_container \
  -p 2368:2368 \
  --mount type=volume,source=ghost_volume,target=/home/node/server/content \
  ghost_image
```

### inspect the container

```bash
# inspect the container
docker exec -i -t ghost_container /bin/sh --login 
```


Docker cleanup
====

### stop the container

```bash
# stop the container 
docker stop -t 0 ghost_container
```

### remove the volume

```bash
# remove volume
docker volume rm content
```