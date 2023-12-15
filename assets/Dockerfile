ARG BUILD_ARG_PYTHON_VERSION=3.8
ARG BUILD_ARG_DEBIAN_VERSION="bookworm"

# Main build environment

FROM python:${BUILD_ARG_PYTHON_VERSION}-${BUILD_ARG_DEBIAN_VERSION} AS base

ARG BUILD_ARG_CONTAINER_GID=1000
ARG BUILD_ARG_CONTAINER_UID=1000

LABEL environment="base"
LABEL maintainer="niall@niallbyrne.ca"
LABEL project="pi_portal"

LABEL org.opencontainers.image.source="https://github.com/pi-portal/pi_portal"
LABEL org.opencontainers.image.description="Development environment for the pi_portal project."

ENV PYTHONUNBUFFERED 1
ENV PROJECT_NAME "pi_portal"

ENV MINIMUM_POETRY=">=1.1.0"

# Mark Container
RUN echo "pi_portal" > /etc/container_release

# Install Base Dependencies
RUN apt-get update          && \
    apt-get upgrade -y      && \
    apt-get install -y         \
    --no-install-recommends    \
    bash                       \
    build-essential            \
    gnupg

# Create the runtime user, and enforce permissions
RUN groupadd user -g "${BUILD_ARG_CONTAINER_GID}" && \
    useradd user -d /home/user                       \
                 -s /bin/bash                        \
                 -u "${BUILD_ARG_CONTAINER_UID}"     \
                 -g "${BUILD_ARG_CONTAINER_GID}"     \
                 -m                                  \
                 -l

# Setup directories
RUN mkdir -p /app             && \
    chown -R user:user /app
WORKDIR /app

# Include the local binary folder in PATH
ENV PATH "/home/user/.local/bin/:${PATH}"


FROM base AS poetry

ARG BUILD_ARG_PIP_INDEX_URL

ENV PIP_INDEX_URL="${BUILD_ARG_PIP_INDEX_URL}"

# hadolint ignore=DL3013
RUN pip install --no-cache-dir "poetry${MINIMUM_POETRY}"

# ======================================================

FROM poetry as pi_portal

# Install Dev Dependencies
RUN apt-get install -y              \
    --no-install-recommends         \
    curl                            \
    fish                            \
    jq                              \
    openssh-client                  \
    sudo                            \
    tig                             \
    vim

# Install LOGZ IO Certificate
# hadolint ignore=DL3059
RUN curl "https://raw.githubusercontent.com/logzio/public-certificates/master/AAACertificateServices.crt" \
    --create-dirs \
    -o /etc/pki/tls/certs/COMODORSADomainValidationSecureServerCA.crt

# Add user to sudoers, and make the default user
# hadolint ignore=DL3059
RUN echo "user ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

COPY assets/dev /usr/local/bin/dev
RUN chmod +x /usr/local/bin/dev         && \
    chown user:user /usr/local/bin/dev

# Set the runtime user
USER user

# ======================================================

FROM pi_portal as development

USER root

# Configure Docker-in-Docker
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
# hadolint ignore=SC1091
RUN install -m 0755 -d /etc/apt/keyrings                                                                                             && \
    curl -fsSL https://download.docker.com/linux/debian/gpg |                                                                           \
    gpg --dearmor -o /etc/apt/keyrings/docker.gpg                                                                                    && \
    chmod a+r /etc/apt/keyrings/docker.gpg                                                                                           && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian       \
         $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null              && \
    apt-get update                                                                                                                   && \
    apt-get install -y --no-install-recommends docker-ce-cli

USER user

# Copy the poetry configuration
COPY poetry.lock pyproject.toml /app/

# Cache Dependencies (amd64)
RUN poetry install --no-root

# Copy the Codebase
COPY . /app

# Install bash customizations
RUN ln -sf /app/assets/bash/.bash* /home/user

# Setup 'dev' command shim
USER root
RUN ln -sf /app/assets/dev /usr/local/bin/dev
USER user

# Install the project
RUN poetry install

# Patch Pre-Commit for DinD
# hadolint ignore=DL3059
RUN poetry run python -m pre_commit_dind

CMD ["./pi_portal/container_init.sh"]
