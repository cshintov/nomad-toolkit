FROM gcr.io/prysmaticlabs/prysm/beacon-chain:v3.2.0 as upstream

FROM debian:buster-slim
COPY --from=upstream /app /app

RUN apt-get update && apt-get install -y \
    curl \
    jq \
    nano \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

ADD scripts/ /opt/tatum.io

STOPSIGNAL SIGINT

ENTRYPOINT ["/app/cmd/beacon-chain/beacon-chain"]
