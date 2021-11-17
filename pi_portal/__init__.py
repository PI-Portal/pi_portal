"""Pi Portal Raspberry Pi door logger."""

from pi_portal.modules import config_file

configuration = config_file.UserConfiguration()
user_config = configuration.load()
