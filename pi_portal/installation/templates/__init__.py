"""Templates for the Pi Portal installation process."""

from typing import List

from pi_portal import config
from .config_file import ConfileFileTemplate

common_templates: List[ConfileFileTemplate] = [
    ConfileFileTemplate(
        source='shim/portal',
        destination=config.PI_PORTAL_SHIM,
        permissions="755"
    ),
    ConfileFileTemplate(
        source='supervisor/supervisord.conf',
        destination=config.PATH_SUPERVISOR_CONFIG,
    ),
]

logzio_templates: List[ConfileFileTemplate] = [
    ConfileFileTemplate(
        source='logzio/filebeat.yml',
        destination=config.PATH_FILEBEAT_CONFIG,
        user=config.PI_PORTAL_USER,
    ),
]

motion_templates: List[ConfileFileTemplate] = [
    ConfileFileTemplate(
        source='motion/motion.conf',
        destination=config.PATH_CAMERA_CONFIG,
        user=config.PI_PORTAL_USER,
    ),
]
