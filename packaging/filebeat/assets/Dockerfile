FROM --platform=${BUILDPLATFORM} debian:bookworm-slim AS filebeat-source

ARG BUILD_ARG_FILEBEAT_VERSION

ENV GOLANG_VERSION="1.21.5"
ENV GO111MODULE="on"
ENV GOPATH="/root/go"

LABEL environment="filebeat-builder"
LABEL maintainer="niall@niallbyrne.ca"
LABEL project="pi_portal"

LABEL org.opencontainers.image.source="https://github.com/pi-portal/pi_portal"
LABEL org.opencontainers.image.description="Filebeat binary builder for pi_portal."

RUN apt-get update          && \
    apt-get install -y         \
    --no-install-recommends    \
    ca-certificates            \
    curl                       \
    git

RUN mkdir -p /root/go
WORKDIR /root/go

RUN curl -L "https://go.dev/dl/go${GOLANG_VERSION}.linux-amd64.tar.gz" -o "go.tar.gz"  && \
    tar -C /usr/local -xzf "go.tar.gz"                                                 && \
    rm go.tar.gz

RUN git clone --depth 1 --branch "v${BUILD_ARG_FILEBEAT_VERSION}" https://github.com/elastic/beats
WORKDIR /root/go/beats/filebeat

RUN /usr/local/go/bin/go mod tidy

# ======================================================

from filebeat-source as filebeat-builder

ARG BUILD_ARG_GOARCH
ARG BUILD_ARG_GOARM
ARG BUILD_ARG_GOOS

RUN env GOARCH="${BUILD_ARG_GOARCH}" GOARM="${BUILD_ARG_GOARM}" GOOS="${BUILD_ARG_GOOS}"  /usr/local/go/bin/go build

# ======================================================

from --platform=${BUILDPLATFORM} debian:bookworm-slim as filebeat-binary

LABEL environment="filebeat"
LABEL maintainer="niall@niallbyrne.ca"
LABEL project="pi_portal"

LABEL org.opencontainers.image.source="https://github.com/pi-portal/pi_portal"
LABEL org.opencontainers.image.description="Distributable filebeat binary for pi_portal."

COPY --from=filebeat-builder /root/go/beats/filebeat/filebeat /usr/bin/filebeat
