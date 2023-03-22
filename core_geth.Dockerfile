FROM etclabscore/core-geth:v1.12.10

RUN apk add curl jq bash nano netcat-openbsd --no-cache

ADD scripts/ /opt/tatum.io

STOPSIGNAL SIGINT
