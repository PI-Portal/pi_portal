"""Core configuration settings."""

import os

PI_PORTAL_INSTALL_LOCATION = os.getenv(
    "PI_PORTAL_INSTALL_LOCATION",
    "/opt/venvs/pi_portal",
)

PI_PORTAL_TASK_MANAGER_CONCURRENCY_LIMIT = 10
PI_PORTAL_TASK_MANAGER_SOCKET = os.path.join(
    PI_PORTAL_INSTALL_LOCATION,
    "socket",
    "uvicorn.sock",
)

CRON_INTERVAL_DEAD_MAN_SWITCH = 60
CRON_INTERVAL_DISK_SPACE = 60 * 10
CRON_INTERVAL_LOGS_UPLOAD = 60 * 60
CRON_INTERVAL_MANIFEST_METRICS = 60 * 30
CRON_INTERVAL_QUEUE_MAINTENANCE = 60 * 60 * 24
CRON_INTERVAL_QUEUE_METRICS = 60 * 30
CRON_INTERVAL_VIDEO_UPLOAD = 60 * 10

LOG_FILE_BASE_FOLDER = "/var/log/pi_portal"
LOG_FILE_CAMERA = f"{LOG_FILE_BASE_FOLDER}/pi_portal.camera.log"
LOG_FILE_CONTACT_SWITCH_MONITOR = (
    f"{LOG_FILE_BASE_FOLDER}/pi_portal.contact_switch.log"
)
LOG_FILE_DEAD_MAN_SWITCH = (
    f"{LOG_FILE_BASE_FOLDER}/pi_portal.dead_man_switch.log"
)
LOG_FILE_TASK_SCHEDULER = f"{LOG_FILE_BASE_FOLDER}/pi_portal.tasks.log"
LOG_FILE_CHAT_BOT = f"{LOG_FILE_BASE_FOLDER}/pi_portal.chat_bot.log"
LOG_FILE_CHAT_CLIENT = f"{LOG_FILE_BASE_FOLDER}/pi_portal.chat_client.log"
LOG_FILE_TEMPERATURE_MONITOR = (
    f"{LOG_FILE_BASE_FOLDER}/pi_portal.temperature.log"
)

LOG_PREFIX_SUPERVISOR = "/var/log/supervisor/supervisor"

PATH_ARCHIVAL_QUEUE_LOG_UPLOAD = os.path.join(
    PI_PORTAL_INSTALL_LOCATION,
    "queue_logs",
)
PATH_ARCHIVAL_QUEUE_VIDEO_UPLOAD = os.path.join(
    PI_PORTAL_INSTALL_LOCATION,
    "queue_videos",
)
PATH_CAMERA_BINARY = "/usr/bin/motion"
PATH_CAMERA_CONFIG = "/etc/motion/motion.conf"
PATH_CAMERA_CONTENT = "/var/lib/motion"
PATH_CAMERA_RUN = "/var/run/motion"
PATH_FILEBEAT_BINARY = os.getenv(
    "PI_PORTAL_FILEBEAT_LOCATION",
    "/usr/bin/filebeat",
)
PATH_FILEBEAT_CONFIG = "/etc/filebeat/filebeat.yml"
PATH_FILEBEAT_CONTENT = "/var/lib/filebeat"
PATH_SUPERVISOR_CONFIG = "/etc/supervisor/supervisord.conf"
PATH_SUPERVISOR_SOCKET = "/var/run/supervisor.sock"
PATH_TASKS_SERVICE_DATABASES = os.path.join(
    PI_PORTAL_INSTALL_LOCATION,
    "db",
)
PATH_USER_CONFIG = "/etc/pi_portal/config.json"

PID_FILE_MOTION = os.path.join(
    PATH_CAMERA_RUN,
    "motion.pid",
)
PID_FILE_SUPERVISORD = '/var/run/supervisord.pid'

PI_PORTAL_SHIM = "/usr/bin/portal"
PI_PORTAL_USER = "pi_portal"
