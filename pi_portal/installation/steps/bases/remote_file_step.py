"""RemoteFileStepBase class."""

import abc
import dataclasses
from concurrent.futures import FIRST_EXCEPTION, Future, ThreadPoolExecutor, wait
from typing import List

from pi_portal.modules.integrations.network import http
from pi_portal.modules.system import file_security, file_system
from . import base_step


@dataclasses.dataclass
class RemoteFile:
  """Maps a remote URL to a local file path target.

  :param sha256: The expected sha256 digest of the file.
  :param target: The local path to write the file to.
  :param url: The remote url to source the file content from.
  :param permissions: The file permissions to set on the downloaded file.
  :param user: The linux user to set as the owner and group of downloaded file.
  """

  sha256: str
  target: str
  url: str
  permissions: str = "644"
  user: str = "root"


class RemoteFileDownloadError(Exception):
  """Raised when a remote file download fails."""


class RemoteFileStepBase(base_step.StepBase, abc.ABC):
  """Remote file download installer step."""

  remote_files: List[RemoteFile]
  worker_count = 4
  fail_fast = True

  def download(self) -> None:
    """Download the configured remote files for this step."""

    tasks: List["Future[None]"] = []
    executor = ThreadPoolExecutor(max_workers=self.worker_count)
    for remote_file in self.remote_files:
      fut = executor.submit(self._download_remote_file_task, remote_file)
      tasks.append(fut)
    executor.shutdown(wait=not self.fail_fast)
    self._wait(tasks)

  def _download_remote_file_task(self, remote_file: RemoteFile) -> None:
    self.log.info(
        "Download: '%s' -> '%s' ...", remote_file.url, remote_file.target
    )
    try:
      http_client = http.HttpClient(self.log)
      http_client.get(remote_file.url, remote_file.target)
      local_file = file_security.FileSecurity(remote_file.target)
      local_file.sha256(remote_file.sha256)
      fs = file_system.FileSystem(remote_file.target)
      fs.ownership(remote_file.user, remote_file.user)
      fs.permissions(remote_file.permissions)
      self.log.info(f"Download: Successfully saved '{remote_file.target}' !")
    except http.HttpClientError as exc:
      self.log.error(
          "Download: Unable to retrieve remote file from '%s' !",
          remote_file.url
      )
      raise RemoteFileDownloadError(remote_file.url) from exc
    except file_security.FileSecurityViolation as exc:
      self.log.error(
          "Download: Unexpected hash value for file downloaded from '%s' !",
          remote_file.url
      )
      raise RemoteFileDownloadError(remote_file.url) from exc

  def _wait(self, tasks: List["Future[None]"]) -> None:
    fut = wait(tasks, return_when=FIRST_EXCEPTION)
    for task in fut.done:
      task.result()
