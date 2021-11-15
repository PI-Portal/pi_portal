# Project Documentation

## pi-portal

Raspberry PI Door Logger

[Project Documentation](https://pi_portal.readthedocs.io/)

### Master Branch Builds (Staging Environment)
- [![pi_portal Generic Push](https://github.com/niall-byrne/pi_portal/workflows/pi_portal-push-generic/badge.svg?branch=master)](https://github.com/niall-byrne/pi_portal/actions)
- [![pi_portal Wheel Push](https://github.com/niall-byrne/pi_portal/workflows/pi_portal-push-wheel/badge.svg?branch=master)](https://github.com/niall-byrne/pi_portal/actions)

### Production Branch Builds (Tags Created on Production Branch)
- [![pi_portal Generic Push](https://github.com/niall-byrne/pi_portal/workflows/pi_portal-push-generic/badge.svg?branch=production)](https://github.com/niall-byrne/pi_portal/actions)
- [![pi_portal Wheel Push](https://github.com/niall-byrne/pi_portal/workflows/pi_portal-push-wheel/badge.svg?branch=production)](https://github.com/niall-byrne/pi_portal/actions)

### Release Builds
- [![pi_portal Release Container](https://github.com/niall-byrne/pi_portal/workflows/pi_portal-release-container/badge.svg)](https://github.com/niall-byrne/pi_portal/actions)
- [![pi_portal Release Wheel](https://github.com/niall-byrne/pi_portal/workflows/pi_portal-release-wheel/badge.svg)](https://github.com/niall-byrne/pi_portal/actions)

## Quick Start Guide

You'll need to install:
 - [Docker](https://www.docker.com/) 
 - [Docker Compose](https://docs.docker.com/compose/install/)
 - [cookiecutter](https://cookiecutter.readthedocs.io/en/latest/)
 - [poetry](https://python-poetry.org/)

Build the development environment container (this takes a few minutes):
- `docker-compose build`

Start the environment container:
- `docker-compose up -d`

Spawn a shell inside the container:
- `./container`

## Tooling Reference
The CLI is installed by default inside the container, and is also available on the host machine.
Run the CLI without arguments to see the complete list of available commands: `dev`

[The 'pib_cli' Python Package](https://pypi.org/project/pib-cli/)

The local CLI configuration is managed by the [cli.yml](./assets/cli.yml) file.

## Environment
The [local.env](./assets/local.env) file can be modified to inject environment variable content into the container.

You can override the values set in this file by setting shell ENV variables prior to starting the container:
- `export GIT_HOOKS_PROTECTED_BRANCHES='.*'`
- `docker-compose kill` (Kill the current running container.)
- `docker-compose rm` (Remove the stopped container.)
- `docker-compose up -d` (Restart the dev environment, with a new container, containing the override.)
- `./container`

## Git Hooks
Git hooks are installed that will enforce linting and unit-testing on the specified branches.

The following environment variables in the  [local.env](./assets/local.env) file can be used to customize this behavior:
- `GIT_HOOKS` (Set this value to 1 to enable the pre-commit hook)
- `GIT_HOOKS_PROTECTED_BRANCHES` (Customize this regex to specify the branches that should enforce the Git Hook on commit.)

Once installed, the hooks required the presence of `pib_cli`, so either inside the container, or with the help of the `pib_setup_hostmachine` command (documented below). 

Use the [scripts/extras.sh](scripts/extras.sh) script to install the hooks:

- `source scripts/extras.sh`
- `install_git_hooks`

## Installing a virtual environment, and the CLI on your host machine

The [scripts/extras.sh](scripts/extras.sh) script does this for you.

Source this script, and use the `dev` command on your host:
- `pip install poetry`
- `source scripts/extras.sh`
- `pib_setup_hostmachine` (to install the poetry dependencies)  
- `dev --help` (to run the cli outside the container)

This is most useful for making an IDE like pycharm aware of what's installed in your project.

> It is still recommended to work inside the container, as you'll have access to the full managed python environment, 
> as well as any additional services you are running in containers.  

If you wish to use the cli outside the container for all tasks, [tomll](https://github.com/pelletier/go-toml) and [gitleaks](https://github.com/zricethezav/gitleaks) will also need to be installed, or the [cli.yml](./assets/cli.yml) configuration will need to be customized to remove these commands. (Not recommended.)
