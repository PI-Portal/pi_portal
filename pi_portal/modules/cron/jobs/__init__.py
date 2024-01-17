"""Pi Portal cron job implementations."""

from typing import List, Type

from ..bases.job import CronJobBase
from . import dead_man_switch, log_upload, video_upload

cron_jobs: List[Type[CronJobBase]] = [
    dead_man_switch.DeadManSwitchCronJob,
    log_upload.LogFileUploadCronJob,
    video_upload.VideoUploadCronJob,
]
