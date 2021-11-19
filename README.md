# Quick Start Guide

## pi-portal

Raspberry PI Door Logger

Put a contact switch on a door and generate logs, alarms and notifications with your Raspberry PI.  Connect a WebCam and view snapshots and motion activated videos over Slack.

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
 
>You'll be able to use this program with other Raspberry PI versions, but you may need to fork the repository and use different GPIO pins, and [compile filebeat](./scripts/arm/filebeat.sh) with different architecture settings.  I have tested it on Raspberry PI 3.)

2. Contact switches.
> These are available cheaply on ebay, AWS or at your local electronics store. 

> Some examples can be found [here](https://www.burglaryalarmsystem.com/category/magnetic-contact.html).

3. Wiring between the switches and the Raspberry Pi.
> I found female jumper cables made this pretty painless.

```
Out of the box Pi Portal has been configured to support two contact switches:
- GPIO pin 13 for the Front Door input
- GPIO pin 5 for the Back Door input
- GND pins for the other end of each contact switch
```

This configuration can be found [here](pi_portal/config.py).

4. A USB camera or webcam that's compatible with [motion](https://motion-project.github.io/).

> [Many](https://www.lavrsen.dk/foswiki/bin/view/Motion/WorkingDevices) webcams are compatible, and easy to find.

### OS Dependencies

You will need to install the following dependencies:

```bash
sudo apt-get install gcc motion supervisor libffi-dev libssl-dev python3-dev
```

### PAAS Accounts

- An [AWS](https://aws.amazon.com/) account
- A [logz.io](https://logz.io/) account
- A [Slack](https://slack.com) account, with bot app credentials

See [this guide](https://ritikjain1272.medium.com/how-to-make-a-slack-bot-in-python-using-slacks-rtm-api-335b393563cd) for setting up a bot account on Slack.

### AWS Infrastructure

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

### Logz IO Integration

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
  "SLACK_BOT_TOKEN": "...token from slack...",
  "SLACK_CHANNEL": "... proper name of slack channel ...",
  "SLACK_CHANNEL_ID": "... slack's ID for the channel (found by looking at the channel's url in a browser) ...",
  "LOGZ_IO_CODE": "... logz io's logger code (for filebeat)...",
  "S3_BUCKET_NAME": "... s3 bucket name (for video archival) ..."
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
