ARG BUILD_ARG_PLATFORM="x86"
ARG BUILD_ARG_PYTHON_VERSION=3.8

# Main build environment

FROM python:${BUILD_ARG_PYTHON_VERSION}-slim AS base

ARG BUILD_ARG_CONTAINER_GID=1000
ARG BUILD_ARG_CONTAINER_UID=1000

LABEL maintainer="niall@niallbyrne.ca"
LABEL project="pi_portal"

ENV PYTHONUNBUFFERED 1
ENV PROJECT_NAME "pi_portal"

ENV MINIMUM_POETRY=">=1.2.0"

# Mark Container
RUN echo "pi_portal" > /etc/container_release

# Install Base Dependencies
RUN apt-get update      && \
    apt-get upgrade -y  && \
    apt-get install -y     \
    bash                   \
    build-essential

# Create the runtime user, and enforce permissions
RUN groupadd user -g "${BUILD_ARG_CONTAINER_GID}"
RUN useradd user -d /home/user                    \
                 -s /bin/bash                     \
                 -u "${BUILD_ARG_CONTAINER_UID}"  \
                 -g "${BUILD_ARG_CONTAINER_GID}"  \
                 -m

# Setup directories
RUN mkdir -p /app
RUN chown -R user:user /app
WORKDIR /app

# Include the local binary folder in PATH
ENV PATH "/home/user/.local/bin/:${PATH}"


FROM base AS poetry

ARG BUILD_ARG_PIP_INDEX_URL

ENV PIP_INDEX_URL="${BUILD_ARG_PIP_INDEX_URL}"

RUN pip install --no-cache-dir "poetry${MINIMUM_POETRY}"

# ======================================================

FROM poetry as pi_portal

ARG BUILD_ARG_PLATFORM

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
RUN curl "https://raw.githubusercontent.com/logzio/public-certificates/master/AAACertificateServices.crt" \
    --create-dirs \
    -o /etc/pki/tls/certs/COMODORSADomainValidationSecureServerCA.crt

# Add user to sudoers, and make the default user
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
RUN install -m 0755 -d /etc/apt/keyrings                                                                                             && \
    curl -fsSL https://download.docker.com/linux/debian/gpg |                                                                           \
    gpg --dearmor -o /etc/apt/keyrings/docker.gpg                                                                                    && \
    chmod a+r /etc/apt/keyrings/docker.gpg                                                                                           && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian       \
         $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null              && \
    apt-get update                                                                                                                   && \
    apt-get install -y docker-ce-cli

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

CMD ["./pi_portal/container_init.sh"]
