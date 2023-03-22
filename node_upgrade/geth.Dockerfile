FROM ethereum/client-go:v1.11.3

RUN apk add curl jq bash nano netcat-openbsd --no-cache && \
    curl -s https://api.github.com/repos/vipnode/vipnode/releases | \
      grep -om1 "https://.*/vipnode-linux_amd64.tgz" | xargs curl -sL | tar vxz

ADD scripts/ /opt/tatum.io

STOPSIGNAL SIGINT
