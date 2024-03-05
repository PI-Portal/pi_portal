# Installing Pi Portal

There are a variety of ways to get up and running with pi_portal depending on the linux distribution you're running.

## General Notes and Troubleshooting Tips

### USB Webcams

This might save someone some trouble…

In some cases unplugging and then reconnecting USB web cameras may renumber the devices.  This changes  their hardware device name.  Since the pi_portal configuration needs to match the hardware device names, this can occasionally cause problems.  

For reliability, it's recommended to avoid these types of disconnections while using the application.  If this scenario does occur, restarting your Raspberry Pi will restore the original device numbering.

### Supervisord

Pi Portal makes heavy use of [supervisord](http://supervisord.org/) to manage processes.

If you have custom configuration for supervisord you will encounter problems during install and uninstall.  Deploying Pi Portal as a docker container is strongly recommended in these types of scenarios.

### Older Hardware

On older Raspberry Pi hardware you should give the supervisor processes plenty of time to startup.  Once they are fully loaded any excessive CPU usage should drop off.

## Installation Method 1: Docker Container

This is probably the simplest approach, but requires [installing docker](https://docs.docker.com/engine/install/raspberry-pi-os/). It's recommended to use a Raspberry PI OS docker host to eliminate possible problems with GPIO or video hardware access inside the container.

Steps:
1. Create a configuration file based on your Slack Bot and GPIOs.
2. Identify the GPIO device.  On Raspberry PI OS this is `/dev/gpiomem`.
3. Identify the video devices of your webcams.  Usually this is `/dev/video0` or similar.
4. Find your [timezone identifier](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).
5. Install the container as a service:

   ```shell
   docker run \
     -d \
     --restart unless-stopped \
     --device [your_gpio_device_name] \
     --device [your_webcam_device_name] \
     -e TZ=[your_timezone_identifier] \
     -v ${PWD}/[your_config_file.json]:/config.json \
     ghcr.io/pi-portal/pi-portal:latest
   ```

6. Log into Slack and start interacting with your camera and sensors.

**Important Note**:
- Any user who is a member of the `docker` group will have full access to the container!
- This includes snapshots, videos and credentials you've installed.

**Other Operating Systems**:
- You will run into problems if your linux distribution is missing the `gpio` or `video` groups:
  - The docker image expects the GPIO hardware (usually `/dev/gpiomem`) to belong to the `gpio` group.
  - The docker image also expects the video hardware (usually `/dev/video0`) to belong to the `video` group.
- For this reason it's recommended to run the container on a Raspberry PI OS system.  It's possible to add these groups via [udevadm](https://manpages.debian.org/bookworm/udev/udevadm.8.en.html), but keep in mind this will complicate your deployment.

## Installation Method 2: Raspberry PI OS

The pi_portal Debian packages are also fairly straightforward to install:

Steps:
1. Identify your CPU architecture:

   ```shell
   uname -m
   ```

2. Identify the underlying Debian version of your Raspberry PI OS install:

   ```shell
   cat /etc/os-release
   ```

3. Visit the pi_portal [latest release page](https://github.com/PI-Portal/pi_portal/releases/latest) and download the corresponding Debian package.
4. Assume root privileges:

   ```shell
   sudo su
   ```

5. Install the Debian package:

   ```shell
   # as root
   apt update
   apt install ./pi-portal_x.x.x-[architecture]_[distribution].deb
   ```

6. Create a configuration file based on your Slack Bot and GPIOs.
7. Find your [timezone identifier](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).  This may already be configured on your system, check the value of the TZ environment variable.
8. Install your configuration file:

   ```shell
   # as root
   export TZ=[your_timezone_identifier] # If necessary ...
   portal install_config [your_config_file.json]
   ```

9. Test your installation:

   ```shell
   # as root
   portal version
   ```

10. Drop root privileges:

    ```shell
    # as root
    exit
    ```

11. Log into Slack and start interacting with your camera and sensors.

## Installation Method 3: Other Linux Distributions

You'll need to roll up your sleeves a little bit when installing pi_portal manually, but it's not that hard…

Steps:
1. Identify your CPU architecture:

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

5. Install the Python build dependencies. (Commands and exact package names vary by distribution.)<!-- markdown-link-check-disable -->
   - [bash](https://packages.debian.org/bookworm/bash)
   - [build-essential](https://packages.debian.org/bookworm/build-essential)
   - [libffi-dev](https://packages.debian.org/bookworm/libffi-dev)
   - [libssl-dev](https://packages.debian.org/bookworm/libssl-dev)
   - [python3](https://packages.debian.org/bookworm/python3-minimal) (Versions 3.8 through 3.11 are supported.)
   - [python3-dev](https://packages.debian.org/bookworm/python3-dev) (Versions 3.8 through 3.11 are supported.)<!-- markdown-link-check-enable -->
   - Note: you may also need to install packages such as `python3-venv` and `python3-pip` if they aren't included in your distribution's core `python3` package.
6. Install the runtime dependencies. (Commands and exact package names vary by distribution.)<!-- markdown-link-check-disable -->
   - [ca-certificates](https://packages.debian.org/bookworm/ca-certificates)
   - [libgpiod2](https://packages.debian.org/bookworm/libgpiod2)
   - [libsqlite3-0](https://packages.debian.org/bookworm/libsqlite3-0)
   - [motion](https://packages.debian.org/bookworm/motion)
   - [supervisor](https://packages.debian.org/bookworm/supervisor)
   - [tzdata](https://packages.debian.org/bookworm/tzdata)<!-- markdown-link-check-enable -->
7. It would be prudent to stop any services launched for motion or supervisor at this point.  
   - The installer will attempt this as well, but your distribution may have an incompatible init system.
8. Create the pi_portal user:

   ```shell
   # as root
   useradd pi_portal --no-create-home -s /bin/false -l
   ```

9. Take a minute and determine what the `gpio` system group is on your system:
   - This linux system group is added to `/dev/gpiomem` or similarly named devices to allow non-root access to GPIO hardware.
   - The user `pi_portal` needs to be a member of this group.

   ```shell
   # as root
   usermod -a -G gpio pi_portal
   ```

   This group may be named differently, or may not exist at all.  Creating this group yourself is possible, via [udevadm](https://manpages.debian.org/bookworm/udev/udevadm.8.en.html).
10. Repeat this same process and identify what the `video` group is on your system:
    - This linux system group allows non-root access to video hardware.
    - The user `pi_portal` needs to be a member of this group.

    ```shell
    # as root
    usermod -a -G video pi_portal
    ```

    This group may be named differently, or may not exist at all.  Creating this group yourself is possible, via [udevadm](https://manpages.debian.org/bookworm/udev/udevadm.8.en.html).
11. Create a configuration file based on your Slack Bot and GPIOs.
12. Install the pi_portal wheel:

    ```shell
    # as root
    mkdir -p /opt/venvs
    python3 -m venv /opt/venvs/pi_portal 
    source /opt/venvs/pi_portal/bin/activate
    pip install ./pi_portal-x.x.x-py3-none-any.whl
    chown -R pi_portal:pi_portal /opt/venvs/pi_portal
    chmod -R o=- /opt/venvs/pi_portal
    ```

    - It's possible to change the location by setting an [environment variable](../pi_portal/config.py).
13. Find your [timezone identifier](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).  This may already be configured on your system, check the value of the TZ environment variable.
14. While still acting as root, install your configuration file:

    ```shell
    # as root
    export TZ=[your_timezone_identifier] # If necessary ...
    pi_portal install_config [your_config_file.json]
    ```

15. Confirm your installation was successful:

    ```shell
    # as root
    portal version
    ```

16. Drop root privileges:

    ```shell
    # as root
    exit
    ```

17. You may need to manually start the supervisor service if the installer doesn't recognize your init system.
18. Log into Slack and start interacting with your camera and sensors.
