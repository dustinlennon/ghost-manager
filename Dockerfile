FROM node:18-alpine AS ghost

# To mount a local directory as a rw volume, the UID and GROUP in the image need
# to match those of the host.  This is made more complicated because the base
# image uses the 1000 UID which is the default in a single user host scenario.
# Thus, if we want a 'ghost' user on the container, we need a corresponding user
# the host with matching UID and GID.
ARG UID=2368
ARG GID=2368

RUN addgroup -g $GID ghost
RUN adduser -G ghost -D -u $UID ghost
RUN echo "umask 0002" > /home/ghost/.profile
# RUN echo "ghost:foo" | chpasswd

# Install git
RUN apk add --no-cache git

# Install ghost framework
RUN npm install ghost-cli -g

# All future commands should run as "node" user
USER ghost
WORKDIR /home/ghost

# Create a location for the server install
RUN mkdir /home/ghost/server
WORKDIR /home/ghost/server

# install ghost
RUN ghost install --version 5.96.2 --no-setup

# # Ref: https://ghost.org/docs/ghost-cli/#
ARG ENDPOINT
RUN ghost setup --db sqlite3 --port 2368 --ip 0.0.0.0 --url $ENDPOINT --process local --no-prompt --no-setup-ssl --no-setup-nginx --no-start

# # # TODO: maybe mv instead of rm?
RUN rm -rf /home/ghost/server/content
# RUN mkdir -p /home/ghost/archive
# RUN mv /home/ghost/server/content /home/ghost/archive/content
VOLUME /home/ghost/server/content

# keepalive (for developing)
# ENTRYPOINT ["tail", "-f", "/dev/null"]
ENTRYPOINT ["ghost", "run"]
