FROM node:18-alpine AS ghost

# The "node" user happens to have UID:1000 GID:1000, and this needs to match
# the host system in order to to get correct ownership when mounting a local 
# share.  There are a few of the uid/gid flags mentioned in the mount man 
# page but neither ext4 nor bind seem to use them.
ARG username=node

# RUN apk upgrade --no-cache
RUN apk add --no-cache git
RUN npm install ghost-cli -g

# All future commands should run as "node" user
USER $username

# Create directories
RUN mkdir -p /home/$username/themes
RUN mkdir -p /home/$username/server
RUN mkdir -p /home/$username/attic

# get digest theme installed  https://github.com/TryGhost/Themes
COPY --chown=node ./themes /home/$username/themes
WORKDIR /home/$username/themes/digest
RUN yarn

# create a local server [ref](https://ghost.org/docs/install/local/)
WORKDIR /home/$username/server
RUN ghost install local --ip 0.0.0.0

WORKDIR /home/$username

# TODO: maybe mv instead of rm?
RUN mv /home/$username/server/content /home/$username/attic
VOLUME /home/$username/server/content

# keepalive (for developing)
ENTRYPOINT ["tail", "-f", "/dev/null"]
