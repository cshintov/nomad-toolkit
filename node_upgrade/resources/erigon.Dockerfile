FROM thorax/erigon:v2.40.1

USER root
RUN apk add curl jq bash nano netcat-openbsd --no-cache
    # && \
    # curl -s https://api.github.com/repos/vipnode/vipnode/releases | \
    #   grep -om1 "https://.*/vipnode-linux_amd64.tgz" | xargs curl -sL | tar vxz

ADD scripts/ /opt/tatum.io

RUN addgroup -g 3473 old-erigon-group
RUN addgroup erigon old-erigon-group
USER erigon

STOPSIGNAL SIGINT
