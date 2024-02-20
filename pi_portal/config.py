"""Core configuration settings."""

import os

PI_PORTAL_INSTALL_LOCATION = os.getenv(
    "PI_PORTAL_INSTALL_LOCATION",
    "/opt/venvs/pi_portal",
)

PI_PORTAL_TASK_MANAGER_SOCKET = os.path.join(
    PI_PORTAL_INSTALL_LOCATION,
    "socket",
    "uvicorn.sock",
)

CRON_INTERVAL_DEAD_MAN_SWITCH = 60
CRON_INTERVAL_LOGS_UPLOAD = 60 * 60
CRON_INTERVAL_QUEUE_MAINTENANCE = 60 * 60 * 24
CRON_INTERVAL_QUEUE_METRICS = 60 * 30
CRON_INTERVAL_VIDEO_UPLOAD = 60 * 10

FILE_BEAT_BINARY = os.getenv("PI_PORTAL_FILEBEAT_LOCATION", "/usr/bin/filebeat")
FILE_BEAT_CONFIG = "/etc/filebeat/filebeat.yml"

LOG_FILE_BASE_FOLDER = "/var/log/pi_portal"
LOG_FILE_CONTACT_SWITCH_MONITOR = (
    f"{LOG_FILE_BASE_FOLDER}/pi_portal.contact_switch.log"
)
LOG_FILE_DEAD_MAN_SWITCH = (
    f"{LOG_FILE_BASE_FOLDER}/pi_portal.dead_man_switch.log"
)
LOG_FILE_MOTION = f"{LOG_FILE_BASE_FOLDER}/pi_portal.motion.log"
LOG_FILE_TASK_SCHEDULER = f"{LOG_FILE_BASE_FOLDER}/pi_portal.tasks.log"
LOG_FILE_CHAT_BOT = f"{LOG_FILE_BASE_FOLDER}/pi_portal.chat_bot.log"
LOG_FILE_CHAT_CLIENT = f"{LOG_FILE_BASE_FOLDER}/pi_portal.chat_client.log"
LOG_FILE_TEMPERATURE_MONITOR = (
    f"{LOG_FILE_BASE_FOLDER}/pi_portal.temperature.log"
)

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
PATH_TASKS_SERVICE_DATABASES = os.path.join(
    os.path.dirname(__file__),
    "modules",
    "tasks",
    "db",
)
PATH_USER_CONFIG = "/etc/pi_portal/config.json"

PID_FILE_MOTION = '/var/run/motion/motion.pid'
PID_FILE_SUPERVISORD = '/var/run/supervisord.pid'

PI_PORTAL_SHIM = "/usr/bin/portal"
PI_PORTAL_USER = "pi_portal"
