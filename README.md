# Quick Start Guide

## pi-portal

Raspberry PI Door Logger

Put a contact switch on a door and generate logs, alarms and notifications with your Raspberry PI.  Connect a WebCam and view snapshots and motion activated videos over Slack.  Add DHT11 temperature sensors and track temperature and humidity fluctuations over time.

This is a hobby solution, and no warranty or guarantees of any kind are made.  Please use at your own risk.

[Project Documentation](https://pi_portal.readthedocs.io/)

### Master Branch Builds (Staging Environment)
- [![pi_portal Generic Push](https://github.com/pi-portal/pi_portal/workflows/pi_portal-push-generic/badge.svg?branch=master)](https://github.com/pi-portal/pi_portal/actions)

### Production Branch Builds (Tags Created on Production Branch)
- [![pi_portal Generic Push](https://github.com/pi-portal/pi_portal/workflows/pi_portal-push-generic/badge.svg?branch=production)](https://github.com/pi-portal/pi_portal/actions)

## Requirements

### Hardware

1. A Raspberry Pi 3.

>You'll need a Raspberry PI 3, with Raspberry Pi OS or similar installed and reliable internet.
 
>You'll be able to use this program with other Raspberry PI versions, but you may need to [compile filebeat](./scripts/arm/filebeat.sh) with different architecture settings.  I have tested it on Raspberry PI 3.

2. Contact switches.
> These are available cheaply on ebay, AWS or at your local electronics store. 

> Some examples can be found [here](https://www.burglaryalarmsystem.com/category/magnetic-contact.html).

3. Temperature monitors.
> Currently, only the DHT11 is supported, but it's very trivial to add support for the DHT22.

>  You can find out more about these sensors [here](https://learn.adafruit.com/dht).

4. Wiring between the switches, temperature monitor and the Raspberry Pi.
> I found female jumper cables made this pretty painless.

> Edit the [config.json](./config.json) file to customize your pin outs and integrations.

This configuration can be found [here](pi_portal/config.py).

5. A USB camera or webcam that's compatible with [motion](https://motion-project.github.io/).

> [Many](https://www.lavrsen.dk/foswiki/bin/view/Motion/WorkingDevices) webcams are compatible, and easy to find.

### OS Dependencies

You will need to install the following dependencies:

```bash
sudo apt-get install gcc libffi-dev libgpiod2 libssl-dev motion python3-dev supervisor
```

### Python

Supports Python [3.7](https://www.python.org/downloads/release/python-370/), [3.8](https://www.python.org/downloads/release/python-380/), [3.9](https://www.python.org/downloads/release/python-390/) or [3.10](https://www.python.org/downloads/release/python-3100/)

### PAAS Accounts

- An [AWS](https://aws.amazon.com/) account
- A [logz.io](https://logz.io/) account
- A [Slack](https://slack.com) account, with bot app credentials

See [this guide](https://ritikjain1272.medium.com/how-to-make-a-slack-bot-in-python-using-slacks-rtm-api-335b393563cd) for setting up a bot account on Slack.

#### AWS Infrastructure

You'll need to create two S3 buckets:
- one to archive logs
- one to archive motion detection videos

Create two separate sets of credentials with write permissions to each bucket.

The policy for each would look similar to:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllPutObjectActions",
      "Effect": "Allow",
      "Action": ["s3:PutObject","s3:PutObjectAcl", "s3:PutObjectVersionAcl"],
      "Resource": ["arn of a bucket"]
    }
  ]
}
```

One set of credentials will be used by PI Portal for video files, the other by [logz.io](https://logz.io/) for log files.

You can also configure [lifecycle rules](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html) for these buckets to control data retention.  (And it's definately a good idea to ensure they are not publicly accessible!)  

#### Logz IO Integration

[This service](https://logz.io/) has a generous free tier that will allow you to search your logs, and do long term retention in the S3 bucket you created.
You will need to know your accounts `log token`, (check the website on how to configure filbeat to find it.)

Enter your AWS credentials for the logging bucket here, to archive your logs. 

PI Portal ships with a binary for [filebeat](https://www.elastic.co/beats/filebeat) that has compiled for the Raspberry PI 3.  This binary is responsible for streaming your logs to [logz.io](https://logz.io/).  

### Installing The PI Portal Software

Download the Python Wheel, and copy to your Raspberry PI.
Install with:

```bash
sudo pip3 install [wheel file name]
```

### Creating a configuration file

Create a configuration json file that contains the following:

```json
{
    "AWS_ACCESS_KEY_ID": "... AWS key with write access to video bucket ...",
    "AWS_SECRET_ACCESS_KEY": "... AWS secret key with write access to video bucket ...",
    "LOGZ_IO_CODE": "... logz io's logger code ...",
    "S3_BUCKET_NAME": "... s3 video bucket name ...",
    "SLACK_BOT_TOKEN": "...token from slack...",
    "SLACK_CHANNEL": "... proper name of slack channel ...",
    "SLACK_CHANNEL_ID": ".. slack's ID for the channel ...",
    "CONTACT_SWITCHES": [
        {
          "NAME": "... name and pin-out of a GPIO switch...",
          "GPIO": 12
        }
    ], 
    "DHT11_SENSORS": [
        {
          "NAME": "... name and pin-out of a GPIO with a DHT11 connected ...",
          "GPIO": 4
        }
    ]
}
```

### Installing the PI Portal system configuration

You can now run the following command to complete the installation:

```bash
pi_portal installer [configuration json file name]
```

Pi Portal will prompt for SUDO, and then run [this](pi_portal/installation/scripts/install.sh) script to complete the install.


### Logs and Slack Bot

You should now be streaming your logs to [logz.io](https://logz.io/), where you can create custom notifications and integrate with other services.
You will also be receiving notifications on the configured Slack channel whenever a door is opened or closed.

You can also interact with the bot service on the Slack channel, try the command `help` to get started.
