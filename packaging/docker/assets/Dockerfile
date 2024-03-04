ARG BUILD_ARG_SOURCE_IMAGE

# hadolint ignore=DL3006
FROM ${BUILD_ARG_SOURCE_IMAGE} as production

ARG BUILD_ARG_DEBIAN_VERSION
ARG BUILD_ARG_PACKAGING_ARCH

LABEL environment="production"
LABEL maintainer="niall@niallbyrne.ca"
LABEL project="pi_portal"

LABEL org.opencontainers.image.source="https://github.com/pi-portal/pi_portal"
LABEL org.opencontainers.image.description="Raspberry Pi Door Logger."

ENV ENVIRONMENT="PRODUCTION"

WORKDIR /root

# Add pi_portal Debian Package
COPY packaging/debian/dist/pi-portal_*-${BUILD_ARG_PACKAGING_ARCH}_${BUILD_ARG_DEBIAN_VERSION}.deb pi_portal.deb

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install pi_portal
# hadolint ignore=DL3027
RUN apt-get update \
    && apt install --no-install-recommends -y \
      tzdata \
      ./pi_portal.deb \
    && rm pi_portal.deb \
    && rm -rf /var/lib/apt/lists/*

# Install Init
COPY packaging/docker/assets/container_init.sh /container_init.sh

ENTRYPOINT ["/container_init.sh"]
