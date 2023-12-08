FROM --platform=${BUILDPLATFORM} debian:bookworm-slim AS filebeat-source

ENV FILEBEAT_VERSION="8.11.0"
ENV GOLANG_VERSION="1.21.5"
ENV GO111MODULE="on"
ENV GOPATH="/root/go"

RUN apt-get update      && \
    apt-get install -y     \
    curl                   \
    git

RUN mkdir -p /root/go
WORKDIR /root/go

RUN curl -L "https://go.dev/dl/go${GOLANG_VERSION}.linux-amd64.tar.gz" -o "go.tar.gz"  && \
    tar -C /usr/local -xzf "go.tar.gz"                                                 && \
    rm go.tar.gz

RUN git clone --depth 1 --branch "v${FILEBEAT_VERSION}" https://github.com/elastic/beats
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

COPY --from=filebeat-builder /root/go/beats/filebeat/filebeat /usr/bin/filebeat
