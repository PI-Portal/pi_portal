# pi_portal

[![cicd-tools](https://img.shields.io/badge/ci/cd:-cicd_tools-blue)](https://github.com/cicd-tools-org/cicd-tools)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

| Branch                                                                                                                                                                                                                 | Build                                                                                                                                                                                                             |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [main](https://github.com/pi-portal/pi_portal/tree/main)                                                                                                                                                               | [![pi_portal-github-workflow-push](https://github.com/pi-portal/pi_portal/actions/workflows/workflow-push.yml/badge.svg?branch=main)](https://github.com/pi-portal/pi_portal/actions/workflows/workflow-push.yml) |
| [dev](https://github.com/pi-portal/pi_portal/tree/dev)                                                                                                                                                                 | [![pi_portal-github-workflow-push](https://github.com/pi-portal/pi_portal/actions/workflows/workflow-push.yml/badge.svg?branch=dev)](https://github.com/pi-portal/pi_portal/actions/workflows/workflow-push.yml)  |

## A Raspberry PI Door Logger

- Put a contact switch on doors and windows to generate logs, alarms and notifications with your Raspberry PI.
- Connect a WebCam and view snapshots and motion activated videos over Slack.
- Add DHT11 temperature sensors and track temperature and humidity fluctuations over time.

This is a hobby solution, no warranty or guarantee of any kind is made.  

Please use at your own risk.

[Project Documentation](https://pi-portal.readthedocs.io/)

## Requirements

### Hardware

1. A Raspberry Pi.
   - You'll need a Raspberry PI with Raspberry PI OS or similar installed and reliable internet.
   - I developed and tested this project on a Pi 1Bv2 and a Pi 3.
2. Magnetic Contact switches.
   - These are available cheaply on ebay, Amazon or at your local electronics store.
   - Some examples can be found [here](https://www.amazon.com/s?k=magnetic+door+switch).
3. Temperature monitors.
   - Currently, only the DHT11 is supported, but it's trivial to add support for the DHT22.
   - You can find out more about these sensors [here](https://learn.adafruit.com/dht).
4. Wiring between the switches, temperature sensors and the Raspberry Pi's GPIO connectors.
   - Find out more about the Pi's GPIO [here](https://projects.raspberrypi.org/en/projects/physical-computing).
   - Female [jump wires](https://en.wikipedia.org/wiki/Jump_wire) make installing the connections pretty painless. I spliced them to the ends of modular cables (i.e. phone cables) for longer runs.
   - Edit the [config.json](config.json) file to customize your pin outs and integrations.
5. A USB camera or webcam that's compatible with [motion](https://motion-project.github.io/).
   - [Many](https://www.lavrsen.dk/foswiki/bin/view/Motion/WorkingDevices) webcams are compatible and widely available.

### Python

Supports Python [3.8](https://www.python.org/downloads/release/python-380/), [3.9](https://www.python.org/downloads/release/python-390/), [3.10](https://www.python.org/downloads/release/python-3100/) or [3.11](https://www.python.org/downloads/release/python-3110/)

### PAAS Accounts

- An [AWS](https://aws.amazon.com/) account
- A [logz.io](https://logz.io/) account
- A [Slack](https://slack.com) account

Setting up each of these accounts will created credentials that must be entered into the pi_portal [configuration file](#creating-a-configuration-file).

#### Slack

See [this guide](markdown/SLACK_BOT_SETUP.md) for setting up a bot on Slack.

#### AWS Infrastructure

You'll need to create two S3 buckets:
- one to archive logs
- one to archive motion detection videos

It's important to make sure these archival buckets are not publicly accessible!  [This AWS document](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html) offers some guidance on how to achieve this.

Create a set AWS cli credentials with write permissions to both of these buckets.

Use the following template to design your write access policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllPutObjectActions",
      "Effect": "Allow",
      "Action": ["s3:PutObject", "s3:PutObjectAcl", "s3:PutObjectVersionAcl"],
      "Resource": ["arn of a bucket1", "arn of a bucket2"]
    }
  ]
}
```

You can also configure [lifecycle rules](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html) for these buckets to control data retention.  This is useful for tasks such as purging data older than `n` number of days.

#### Logz.io Integration

[This service](https://logz.io/) has a generous free tier that will allow you to search your logs and create useful reports and graphs.
You will need to know your account's `log token`, (check the website on how to configure filebeat to find it.)

pi_portal ships with a binary for [filebeat](https://www.elastic.co/beats/filebeat) that has been compiled for each supported arm platform.  This binary is responsible for streaming your logs to [logz.io](https://logz.io/).

## Creating a configuration file

Once you've setup your PaaS accounts, it's time to get started rolling your own configuration file.  Here's some resources to help:

1. First it's handy to look at the [sample config](config.json) included in the repository.
2. For more detail on what the options all do, there's a JSON schema [documented here](https://pi-portal.readthedocs.io/en/stable/project/5.configuration.html) that can help you make the most of your config.
3. The actual JSON schema is [here](pi_portal/schema/config_schema.json) and is used to do programmatic validation of your configuration.
4. The motion configuration can be a bit overwhelming.  The existing values in the [sample config](config.json) should get you started.  You can also check out the [motion](pi_portal/installation/templates/motion/motion.conf) and individual [camera](pi_portal/installation/templates/motion/camera.conf) configuration files for a bit more information.

## Installing The PI Portal Software

There are 3 primary delivery mechanisms for pi_portal:
- a multiarch (armv6, armv7 and arm64) [docker](https://www.docker.com/) image
- a set of Raspberry PI OS compatible [deb](https://en.wikipedia.org/wiki/Deb_(file_format)) packages
- a Python [wheel](https://packaging.python.org/en/latest/specifications/binary-distribution-format/) and [source distribution](https://packaging.python.org/en/latest/specifications/source-distribution-format/)

Please see the [installation guide](markdown/INSTALLATION.md) for further details.

### Up and Running with Logs and Slack

Once correctly configured and installed, you should be streaming your logs to [logz.io](https://logz.io/).  Using this service you can create custom notifications and integrate with dozens of other remote services.

You will also be receiving notifications on the configured Slack channel whenever a door is opened or closed.  The Slack bot will respond to commands typed into the channel:
- try the command `help` to get started.
