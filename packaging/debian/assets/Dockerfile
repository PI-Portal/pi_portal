ARG BUILD_ARG_PLATFORM

# hadolint ignore=DL3006
# Workaround for docker compose not using local images
FROM debian-packaging:${BUILD_ARG_PLATFORM} as development

ARG BUILD_ARG_FILEBEAT_PLATFORM

LABEL environment="debian-packaging"
LABEL maintainer="niall@niallbyrne.ca"
LABEL project="pi_portal"

LABEL org.opencontainers.image.source="https://github.com/pi-portal/pi_portal"
LABEL org.opencontainers.image.description="Debian binary package builder for pi_portal."

USER root

RUN apt-get install -y      \
    --no-install-recommends \
    debhelper               \
    dh-python               \
    dh-virtualenv           \
    fakeroot                \
    libffi-dev              \
    libgpiod2               \
    libssl-dev              \
    pkg-config              \
    python3-all             \
    python3-dev             \
    python3-setuptools

# hadolint ignore=DL3059
RUN useradd pi-portal       \
    --no-create-home        \
    -s /bin/false           \
    -l

USER user

COPY packaging/filebeat/bin/filebeat-${BUILD_ARG_FILEBEAT_PLATFORM} /usr/bin/filebeat
