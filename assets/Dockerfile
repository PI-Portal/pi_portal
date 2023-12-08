ARG BUILD_ARG_PLATFORM="x86"
ARG BUILD_ARG_PYTHON_VERSION=3.7

# Main build environment

FROM python:${BUILD_ARG_PYTHON_VERSION}-slim AS base

ARG BUILD_ARG_CONTAINER_GID=1000
ARG BUILD_ARG_CONTAINER_UID=1000

LABEL maintainer="niall@niallbyrne.ca"
LABEL project="pi_portal"

ENV PYTHONUNBUFFERED 1
ENV PROJECT_NAME "pi_portal"
ENV PIB_CONFIG_FILE_LOCATION "/app/assets/cli.yml"

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

FROM poetry as development

ARG BUILD_ARG_PLATFORM

# Install Dev Dependencies
RUN apt-get install -y              \
    --no-install-recommends         \
    curl                            \
    fish                            \
    golang-github-pelletier-go-toml \
    jq                              \
    openssh-client                  \
    shellcheck                      \
    sudo                            \
    tig                             \
    vim

# Install LOGZ IO Certificate
RUN curl "https://raw.githubusercontent.com/logzio/public-certificates/master/AAACertificateServices.crt" \
    --create-dirs \
    -o /etc/pki/tls/certs/COMODORSADomainValidationSecureServerCA.crt

# Add user to sudoers, and make the default user
RUN echo "user ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Set the runtime user
USER user

# Copy the poetry configuration
COPY poetry.lock pyproject.toml /app/

# Cache Dependencies (amd64)
RUN if [ "${BUILD_ARG_PLATFORM}" = "amd64" ]; then                        \
      poetry install --no-root -E docs;                                   \
    fi

# Copy the Codebase
COPY . /app

# Create A Symlink For the Bash Customizations
RUN ln -sf /app/assets/.bash_customize /home/user/.bash_customize

# Enforce sane git permissions
USER root
RUN chown -R user:user /app
USER user

# Install The App
RUN if [ "${BUILD_ARG_PLATFORM}" = "amd64" ]; then                         \
      poetry install -E docs                                            && \
      poetry run dev setup-bash;                                           \
    fi

CMD ["./pi_portal/container_init.sh"]
