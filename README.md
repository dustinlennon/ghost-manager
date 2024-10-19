
User/group setup
====

There's some awkward behavior where, in order to mount a local volume, you want the uid and gid to match.  So on the host machine, and in the container, there is a ghost user and a ghost group with uid 2368 and gid 2368.  This needs to be setup on the host machine; the Dockefile takes care of it when building the image.


Logs / Debugging
====

Using `docker logs` and `journalctl -u ghost.docker.service` were helpful for debugging.


