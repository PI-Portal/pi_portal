"""Core configuration settings."""

import os

PI_PORTAL_INSTALL_LOCATION = os.getenv(
    "PI_PORTAL_INSTALL_LOCATION",
    "/opt/venvs/pi_portal",
)

CRON_INTERVAL_DEAD_MAN_SWITCH = 60 * 5
CRON_INTERVAL_VIDEO_UPLOAD = 10

FILE_BEAT_BINARY = os.getenv("PI_PORTAL_FILEBEAT_LOCATION", "/usr/bin/filebeat")
FILE_BEAT_CONFIG = "/etc/filebeat/filebeat.yml"

LOG_FILE_BASE_FOLDER = "/var/log/pi_portal"
LOG_FILE_CRON_SCHEDULER = f"{LOG_FILE_BASE_FOLDER}/pi_portal.cron.log"
LOG_FILE_DOOR_MONITOR = f"{LOG_FILE_BASE_FOLDER}/pi_portal.door.log"
LOG_FILE_MOTION = f"{LOG_FILE_BASE_FOLDER}/pi_portal.motion.log"
LOG_FILE_SLACK_BOT = f"{LOG_FILE_BASE_FOLDER}/pi_portal.slack_bot.log"
LOG_FILE_SLACK_CLIENT = f"{LOG_FILE_BASE_FOLDER}/pi_portal.slack_client.log"
LOG_FILE_TEMPERATURE_MONITOR = \
    f"{LOG_FILE_BASE_FOLDER}/pi_portal.temperature.log"

LOG_PREFIX_SUPERVISOR = "/var/log/supervisor/supervisor"

PATH_MOTION_CONTENT = "/var/lib/motion"
PATH_QUEUE_LOG_UPLOAD = os.path.join(
    PI_PORTAL_INSTALL_LOCATION,
    "queue_logs",
)
PATH_QUEUE_VIDEO_UPLOAD = os.path.join(
    PI_PORTAL_INSTALL_LOCATION,
    "queue_videos",
)
PATH_SUPERVISOR_SOCKET = "/var/run/supervisor.sock"
PATH_USER_CONFIG = "/etc/pi_portal/config.json"

PID_FILE_MOTION = '/var/run/motion/motion.pid'
PID_FILE_SUPERVISORD = '/var/run/supervisord.pid'

PI_PORTAL_SHIM = "/usr/bin/portal"
PI_PORTAL_USER = "pi_portal"
