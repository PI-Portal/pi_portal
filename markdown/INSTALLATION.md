# Installing Pi Portal

There are a variety of ways to get up and running with pi_portal depending on the linux distribution you're running.

On older Raspberry Pi hardware you should give the supervisor processes plenty of time to startup.  Once they are fully loaded any excessive CPU usage should drop off.

## Supervisord Warning

Pi Portal makes heavy use of [supervisord](http://supervisord.org/) to manage processes.

If you have custom configuration for supervisord you will encounter problems during install and uninstall.  Deploying Pi Portal as a docker container is strongly recommended in these types of scenarios.

## Docker Container

This is probably the simplest approach, but requires [installing docker](https://docs.docker.com/engine/install/raspberry-pi-os/):

Steps:
1. Create a configuration file based on your Slack Bot and GPIOs.
2. Install the container as a service:

   ```shell
   docker run \
     -d \
     --restart unless-stopped \
     --device /dev/gpiomem \
     --device /dev/video0 \
     -v ${PWD}/[your_config_file.json]:/config.json \
     ghcr.io/pi-portal/pi-portal:latest
   ```

3. Log into Slack and start interacting with your camera and sensors.

**Important Note**:
- Anyone user who is a member of the `docker` group will have full access to the container!

## Raspberry PI OS

The pi_portal Debian packages are also fairly straightforward to install:

Steps:
1. Identify your CPU architecture

   ```shell
   uname -m
   ```

2. Identify the underlying Debian version of your Raspberry Pi OS install:

   ```shell
   cat /etc/os-release
   ```

3. Visit the pi_portal [latest release page](https://github.com/PI-Portal/pi_portal/releases/latest) and download the corresponding Debian package.
4. Install the Debian package:

   ```shell
   sudo apt update
   sudo apt install ./pi-portal-x.x.x-[architecture]-[distribution].deb
   ```

5. Create a configuration file based on your Slack Bot and GPIOs.
6. Install your configuration file:

   ```shell
   sudo portal install_config [your_config_file.json]
   ```

7. Test your installation:

   ```shell
   sudo portal version
   ```

8. Log into Slack and start interacting with your camera and sensors.

## Other Linux Distributions

You'll need to roll up your sleeves a little bit when installing pi_portal manually, but it's not that hard ...

Steps:
1. Identify your CPU architecture

   ```shell
   uname -m
   ```

2. Visit the pi_portal [latest release page](https://github.com/PI-Portal/pi_portal/releases/latest) and download:
   - the correct filebeat tarball for your CPU
   - the pi_portal python wheel

3. Assume root privileges:

   ```shell
   sudo su
   ```

4. Install filebeat:

   ```shell
   # as root
   tar xvzf filebeat-linux-[x-x-x]-[architecture].tar.gz -C /usr/bin
   ```

5. Install the Python build dependencies. (Commands and exact package names vary by distribution.)
   - [bash](https://packages.debian.org/bookworm/bash)
   - [build-essential](https://packages.debian.org/bookworm/build-essential)
   - [libffi-dev](https://packages.debian.org/bookworm/libffi-dev)
   - [libssl-dev](https://packages.debian.org/bookworm/libssl-dev)
   - [python3](https://packages.debian.org/bookworm/python3-minimal) (Versions 3.8 through 3.11 are supported.)
   - [python3-dev](https://packages.debian.org/bookworm/python3-dev) (Versions 3.8 through 3.11 are supported.)
   - Note: you may also need to install packages such as `python3-venv` and `python3-pip` if they aren't included in your distribution's core `python3` package.
6. Install the runtime dependencies. (Commands and exact package names vary by distribution.)
   - [ca-certificates](https://packages.debian.org/bookworm/ca-certificates)
   - [libgpiod2](https://packages.debian.org/bookworm/libgpiod2)
   - [motion](https://packages.debian.org/bookworm/motion)
   - [supervisor](https://packages.debian.org/bookworm/supervisor)
7. It would be prudent to stop any services launched for motion or supervisor at this point.  
   - The installer will attempt this as well, but your distribution may have an unknown init system.
8. Create the pi-portal user:

   ```shell
   # as root
   useradd pi-portal --no-create-home -s /bin/false -l
   ```

9. Create a configuration file based on your Slack Bot and GPIOs.
10. Install the pi_portal wheel:

    ```shell
    # as root
    mkdir -p /opt/venvs
    python3 -m venv /opt/venvs/pi-portal 
    source /opt/venvs/pi-portal/bin/activate
    pip install ./pi_portal-x.x.x-py3-none-any.whl
    chown -R pi-portal:pi-portal /opt/venvs/pi-portal
    ```

    - You can customize the location by setting an [environment variable](../pi_portal/config.py).
11. While still acting as root, install your configuration file:

    ```shell
    # as root
    pi_portal install_config [your_config_file.json]
    ```

12. Confirm you install was successful:

    ```shell
    # as root
    portal version
    ```

13. Drop root privileges:

    ```shell
    # as root
    exit
    ```

14. You may need to manually start the supervisor service if the installer doesn't recognize your init system.
15. Log into Slack and start interacting with your camera and sensors.
