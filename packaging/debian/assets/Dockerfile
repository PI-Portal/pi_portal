ARG BUILD_ARG_PLATFORM

FROM ${BUILD_ARG_PLATFORM}-prebuild as development

ARG BUILD_ARG_PLATFORM

USER root

RUN apt-get install -y      \
    debhelper               \
    dh-python               \
    dh-virtualenv           \
    pkg-config              \
    python3-all             \
    python3-dev             \
    python3-setuptools

RUN useradd pi-portal       \
    --no-create-home        \
    -s /bin/false

USER user

COPY packaging/filebeat/bin/filebeat-${BUILD_ARG_PLATFORM} /usr/bin/filebeat
