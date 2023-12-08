"""Templates for the pi_portal installation process."""

from typing import List

from .config_file import ConfileFileTemplate

configuration_templates: List[ConfileFileTemplate] = [
    ConfileFileTemplate(
        source='logzio/filebeat.yml',
        destination='/etc/filebeat/filebeat.yml',
    ),
    ConfileFileTemplate(
        source='motion/motion.conf',
        destination='/etc/motion/motion.conf',
    ),
    ConfileFileTemplate(
        source='supervisor/supervisord.conf',
        destination='/etc/supervisor/supervisord.conf',
    ),
]
