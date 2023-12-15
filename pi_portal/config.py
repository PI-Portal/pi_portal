"""Core configuration settings."""

import os

PI_PORTAL_INSTALL_LOCATION = os.getenv(
    "PI_PORTAL_INSTALL_LOCATION",
    "/opt/venvs/pi-portal",
)

FILE_BEAT_BINARY = os.getenv("PI_PORTAL_FILEBEAT_LOCATION", "/usr/bin/filebeat")
FILE_BEAT_CONFIG = "/etc/filebeat/filebeat.yml"

LOG_FILE_DOOR_MONITOR = "/var/log/pi_portal.door.log"
LOG_FILE_MOTION = "/var/log/pi_portal.motion.log"
LOG_FILE_SLACK_BOT = "/var/log/pi_portal.slack_bot.log"
LOG_FILE_SLACK_CLIENT = "/var/log/pi_portal.slack_client.log"
LOG_FILE_TEMPERATURE_MONITOR = "/var/log/pi_portal.temperature.log"
LOG_FILE_VIDEO_UPLOAD_CRON = "/var/log/pi_portal.video_upload_cron.log"

LOG_PREFIX_SUPERVISOR = "/var/log/supervisor/supervisor"

PATH_MOTION_CONTENT = "/var/lib/motion"
PATH_SUPERVISOR_SOCKET = "/var/run/supervisor.sock"
PATH_USER_CONFIG_INSTALL = os.path.join(
    PI_PORTAL_INSTALL_LOCATION,
    "config.json",
)
PATH_VIDEO_UPLOAD_QUEUE = os.path.join(
    PI_PORTAL_INSTALL_LOCATION,
    "queue_videos",
)

PID_FILE_MOTION = '/var/run/motion/motion.pid'
PID_FILE_SUPERVISORD = '/var/run/supervisord.pid'

PI_PORTAL_SHIM = "/usr/bin/portal"
PI_PORTAL_USER = "pi-portal"
