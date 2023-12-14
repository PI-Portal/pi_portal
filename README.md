## pi_portal

Raspberry PI Door Logger

Put a contact switch on a door and generate logs, alarms and notifications with your Raspberry PI.  Connect a WebCam and view snapshots and motion activated videos over Slack.  Add DHT11 temperature sensors and track temperature and humidity fluctuations over time.

This is a hobby solution, and no warranty or guarantees of any kind are made.  

Please use at your own risk.

[Project Documentation](https://pi-portal.readthedocs.io/)

### Master Branch Builds
- [![pi_portal Generic Push](https://github.com/pi-portal/pi_portal/workflows/pi_portal-push-generic/badge.svg?branch=master)](https://github.com/pi-portal/pi_portal/actions)

### Production Branch Builds
- [![pi_portal Generic Push](https://github.com/pi-portal/pi_portal/workflows/pi_portal-push-generic/badge.svg?branch=production)](https://github.com/pi-portal/pi_portal/actions)

## Requirements

### Hardware

1. A Raspberry Pi 3.
   - You'll need a Raspberry PI with Raspberry Pi OS or similar installed and reliable internet.
2. Contact switches.
   - These are available cheaply on ebay, AWS or at your local electronics store. 
   - Some examples can be found [here](https://www.burglaryalarmsystem.com/category/magnetic-contact.html).
3. Temperature monitors.
   - Currently, only the DHT11 is supported, but it's very trivial to add support for the DHT22.
   -  You can find out more about these sensors [here](https://learn.adafruit.com/dht).
4. Wiring between the switches, temperature monitor and the Raspberry Pi.
   - I found female jumper cables made this pretty painless.
   - Edit the [config.json](./config.json) file to customize your pin outs and integrations.
5. A USB camera or webcam that's compatible with [motion](https://motion-project.github.io/).
   - [Many](https://www.lavrsen.dk/foswiki/bin/view/Motion/WorkingDevices) webcams are compatible, and easy to find.

### OS Dependencies

You will need to install the following dependencies:

```bash
sudo apt-get install gcc libffi-dev libgpiod2 libssl-dev motion python3-dev supervisor
```

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

You can also configure [lifecycle rules](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html) for these buckets to control data retention.  (And it's definitely a good idea to ensure they are not publicly accessible!)  

#### Logz.io Integration

[This service](https://logz.io/) has a generous free tier that will allow you to search your logs, and do long term retention in the S3 bucket you created.
You will need to know your accounts `log token`, (check the website on how to configure filebeat to find it.)

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
    "CONTACT_SWITCHES": [
          {
            "NAME": "... name and pin-out of a GPIO switch...",
            "GPIO": 12
          }
      ],
    "LOGZ_IO_CODE": "... logz io's logger code ...",
    "S3_BUCKET_NAME": "... s3 video bucket name ...",
    "SLACK_APP_SIGNING_SECRET": "... secret value from slack to validate bot messages ...",
    "SLACK_APP_TOKEN": "... token from slack to allow app to use websockets ...",
    "SLACK_BOT_TOKEN": "... token from slack...",
    "SLACK_CHANNEL_ID": ".. slack's ID for the channel ...",
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

### Installing the PI Portal system configuration

To complete the installation, you will need to install the configuration file you created above with pi_portal.

Be advised that existing supervisor and motion configurations will be overwritten, if you have customized these files you should back them up before proceeding.

This command should be run as root, as it will modify system files and protect your configuration file by setting appropriate permissions:

```bash
sudo pi_portal install_config [configuration json file name]
```

### Logs and Slack Bot

You should now be streaming your logs to [logz.io](https://logz.io/), where you can create custom notifications and integrate with other services.
You will also be receiving notifications on the configured Slack channel whenever a door is opened or closed.

You can also interact with the bot service on the Slack channel, try the command `help` to get started.
