"""Core configuration settings."""

FILE_BEAT_BINARY = "/usr/bin/filebeat"
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
PATH_VIDEO_UPLOAD_QUEUE = "/opt/pi_portal/queue_videos"
PATH_USER_CONFIG_INSTALL = "/opt/venvs/pi_portal/config.json"

PID_FILE_MOTION = '/var/run/motion/motion.pid'
PID_FILE_SUPERVISORD = '/var/run/supervisord.pid'

PI_PORTAL_SHIM = "/usr/bin/portal"
PI_PORTAL_USER = "pi-portal"
