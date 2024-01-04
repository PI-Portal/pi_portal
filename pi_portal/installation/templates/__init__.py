"""Templates for the Pi Portal installation process."""

from typing import List

from pi_portal import config
from .config_file import ConfileFileTemplate

common_templates: List[ConfileFileTemplate] = [
    ConfileFileTemplate(
        source='motion/motion.conf',
        destination='/etc/motion/motion.conf',
    ),
    ConfileFileTemplate(
        source='shim/portal',
        destination=config.PI_PORTAL_SHIM,
        permissions="755"
    ),
    ConfileFileTemplate(
        source='supervisor/supervisord.conf',
        destination='/etc/supervisor/supervisord.conf',
    ),
]

logzio_templates: List[ConfileFileTemplate] = [
    ConfileFileTemplate(
        source='logzio/filebeat.yml',
        destination='/etc/filebeat/filebeat.yml',
    ),
]
