

ghost-manager
====

`ghost-manager` is a repo that catalogues the config / tools I'm currently using to manage my Ghost blog.  This runs in a Docker container on a separate machine using systemd to install the blog as a service.  I use letsencrypt for ssl cert.  Apache handles the SSL and provides a reverse proxy to the Ghost blog.


User/group setup
====

There's some awkward Docker behavior where, in order to mount a local volume, you want the uid and gid to match.  So on the host machine, and in the container, there is a ghost user and a ghost group with uid 2368 and gid 2368.  While the Dockefile takes care of this when building the image, this UID/GID needs to be established on the host machine as well.  If these don't match, the shared volume tends to be the culprit for numerous permission denied errors.


Logs / Debugging
====

Maybe obvious, but `docker logs` and `journalctl -u ghost.docker.service` were both helpful for debugging.


simple publishing
====

Put new notebooks and markdown files in their own subdirectory of `./staging`.  With the exception of images, these should be self-contained.  Per-page LaTeX can always be put in a hidden div.

Use a `.env` file to set environment variables; `dotenv` is intended to be an easily modified starting point.  Note that PATH should include a path that contains the scripts from the `ghost-publish` companion package.

Invoke `ghostpub.sh` to set the environment.  Then run `make` within that environment.


## adding a feature image

The ghostpub shell provides a `feature` function for creating a feature.png image.


apache conf
====

Because it was a bit fussy to get working, these are the relevant bits of my apache configuration:

    <VirtualHost *:443>
        SSLEngine on

        # Ghost blog: this was pretty fussy; note "https" on the ghost endpoint
        <Location "/">
            ProxyPreserveHost On
            ProxyPass "http://localhost:2368/"
            ProxyPassReverse "http://localhost:2368/"
            RequestHeader set X-Forwarded-Proto "https"
        </Location>

        # I found it useful to have /ghost-assets/ be a pointer to content; this should make it easier
        # to relocate ghost if ever necessary
        <Location "/ghost-assets/">
            ProxyPreserveHost On
            ProxyPass "http://localhost:2368/content/"
            ProxyPassReverse "http://localhost:2368/content/"
            RequestHeader set X-Forwarded-Proto "https"
        </Location>

        Include /etc/letsencrypt/options-ssl-apache.conf
        SSLCertificateFile /etc/letsencrypt/live/your-host.com-0002/fullchain.pem
        SSLCertificateKeyFile /etc/letsencrypt/live/your-host.com-0002/privkey.pem
    </VirtualHost>

