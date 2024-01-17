# pi_portal

Raspberry PI Door Logger

- Put a contact switch on a door and generate logs, alarms and notifications with your Raspberry PI.  
- Connect a WebCam and view snapshots and motion activated videos over Slack.
- Add DHT11 temperature sensors and track temperature and humidity fluctuations over time.

This is a hobby solution, no warranty or guarantee of any kind is made.  

Please use at your own risk.

[Project Documentation](https://pi-portal.readthedocs.io/)

## Master Branch Builds
- [![pi_portal-github-workflow-push](https://github.com/PI-Portal/pi_portal/actions/workflows/workflow-push.yml/badge.svg?branch=master)](https://github.com/PI-Portal/pi_portal/actions/workflows/workflow-push.yml)

## Production Branch Builds
- [![pi_portal-github-workflow-push](https://github.com/PI-Portal/pi_portal/actions/workflows/workflow-push.yml/badge.svg?branch=production)](https://github.com/PI-Portal/pi_portal/actions/workflows/workflow-push.yml)

## Requirements

### Hardware

1. A Raspberry Pi.
   - You'll need a Raspberry PI with Raspberry Pi OS or similar installed and reliable internet.
   - I developed and tested this project on a Pi 1Bv2 and a Pi 3.
2. Contact switches.
   - These are available cheaply on ebay, Amazon or at your local electronics store.
   - Some examples can be found [here](https://www.burglaryalarmsystem.com/category/magnetic-contact.html).
3. Temperature monitors.
   - Currently, only the DHT11 is supported, but it's very trivial to add support for the DHT22.
   - You can find out more about these sensors [here](https://learn.adafruit.com/dht).
4. Wiring between the switches, temperature monitors and the Raspberry Pi's GPIO connectors.
   - Find out more about the Pi's GPIO [here](https://projects.raspberrypi.org/en/projects/physical-computing).
   - Female [jump wires](https://en.wikipedia.org/wiki/Jump_wire) make installing the connections pretty painless. I spliced them to the ends of modular cables (i.e. phone cables) for longer runs.
   - Edit the [config.json](./config.json) file to customize your pin outs and integrations.
5. A USB camera or webcam that's compatible with [motion](https://motion-project.github.io/).
   - [Many](https://www.lavrsen.dk/foswiki/bin/view/Motion/WorkingDevices) webcams are compatible, and easy to find.

### Python

Supports Python [3.8](https://www.python.org/downloads/release/python-380/), [3.9](https://www.python.org/downloads/release/python-390/), [3.10](https://www.python.org/downloads/release/python-3100/) or [3.11](https://www.python.org/downloads/release/python-3110/)

### PAAS Accounts

- An [AWS](https://aws.amazon.com/) account
- A [logz.io](https://logz.io/) account
- A [Slack](https://slack.com) account, with bot app credentials

See [this guide](markdown/SLACK_BOT_SETUP.md) for setting up your bot on Slack.

#### AWS Infrastructure

You'll need to create two S3 buckets:
- one to archive logs
- one to archive motion detection videos

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

You can also configure [lifecycle rules](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html) for these buckets to control data retention.  (And it's definitely a good idea to ensure they are not publicly accessible!)  

#### Logz.io Integration

[This service](https://logz.io/) has a generous free tier that will allow you to search your logs and create useful reports and graphs.
You will need to know your accounts `log token`, (check the website on how to configure filebeat to find it.)

Enter your AWS credentials for the logging bucket here, to archive your logs.

PI Portal ships with a binary for [filebeat](https://www.elastic.co/beats/filebeat) that has compiled for the Raspberry PI 3.  This binary is responsible for streaming your logs to [logz.io](https://logz.io/).  

## Creating a configuration file

Create a configuration json file that contains the following:

```json
{
  "ARCHIVAL": {
    "AWS": {
      "AWS_ACCESS_KEY_ID": "... AWS key with write access to buckets ...",
      "AWS_SECRET_ACCESS_KEY": "... AWS secret key with write access buckets ...",
      "AWS_S3_BUCKETS": {
        "LOGS": "... s3 logs bucket name ...",
        "VIDEOS": "... s3 video bucket name ..."
      }
    }
  },
  "CHAT": {
    "SLACK": {
      "SLACK_APP_SIGNING_SECRET": "... secret value from slack to validate bot messages ...",
      "SLACK_APP_TOKEN": "... token from slack to allow app to use websockets ...",
      "SLACK_BOT_TOKEN": "... token from slack...",
      "SLACK_CHANNEL": "... proper name of slack channel ...",
      "SLACK_CHANNEL_ID": ".. slack's ID for the channel ..."
    }
  },
  "LOGS": {
    "LOGZ_IO": {
      "LOGZ_IO_TOKEN": "... logz io's logger token ..."
    }
  },
  "SWITCHES": {
    "CONTACT_SWITCHES": [
      {
        "NAME": "... name and pin-out of a GPIO switch...",
        "GPIO": 12
      }
    ]
  },
  "TEMPERATURE_SENSORS": {
    "DHT11": [
      {
        "NAME": "... name and pin-out of a GPIO with a DHT11 connected ...",
        "GPIO": 4
      }
    ]
  }
}
```

## Installing The PI Portal Software

There are 3 primary delivery mechanisms for Pi Portal:
- a multiarch (armv6, armv7 and arm64) [docker](https://www.docker.com/) image
- a set of Raspberry Pi OS compatible [deb](https://en.wikipedia.org/wiki/Deb_(file_format)) packages
- a Python [wheel](https://packaging.python.org/en/latest/specifications/binary-distribution-format/) and [source distribution](https://packaging.python.org/en/latest/specifications/source-distribution-format/)

Please see the [installation guide](markdown/INSTALLATION.md) for further details.

### Up and Running with Logs and Slack Bot

Once configured and installed you should be streaming your logs to [logz.io](https://logz.io/), where you can create custom notifications and integrate with other services.
You will also be receiving notifications on the configured Slack channel whenever a door is opened or closed.

You can also interact with the bot service on the Slack channel, try the command `help` to get started.
