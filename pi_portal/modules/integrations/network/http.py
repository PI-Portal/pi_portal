"""Network utilities for the Pi Portal Project."""

import logging
import shutil
from typing import Optional, Tuple

import requests
import urllib3
from requests import Session
from requests.adapters import HTTPAdapter


class HttpClientError(Exception):
  """Raised when the HTTP client encounters an error."""


class HttpClient:
  """Remote HTTP server client.

  :param log: A logging instance.
  """

  # Be very careful you don't trigger the issue referenced here:
  # https://github.com/advisories/GHSA-pq67-6m6q-mj2v
  # Since you are using requests, and not a PoolManager class this should be ok
  retry_config = urllib3.Retry(5, redirect=5)
  basic_auth: Optional[Tuple[str, str]]

  def __init__(self, log: logging.Logger) -> None:
    self.log = log
    self.basic_auth = None

  def set_basic_auth(self, username: str, password: str) -> None:
    """Set basic authentication on the HTTP request.

    :param username: The username to use for authentication.
    :param password: The password to use for authentication.
    """
    self.basic_auth = (username, password)

  def get(self, url: str, target: Optional[str] = None) -> requests.Response:
    """Fetch a remote URL and save to a local file system target.

    :param url: The remote URL to fetch.
    :param target: The local path to write the content to.
    :returns: The http response object.
    """

    self.log.info(f"HTTP GET: '{url}' ...")

    session = self._create_request_session()

    if self.basic_auth:
      session.auth = self.basic_auth

    response = session.get(url, stream=True)

    if response.ok:
      self.log.info("HTTP GET: Connected to '%s' ...", url)
      if target:
        self._save_response(response, target)
      return response

    self.log.error(
        "HTTP GET: Unable to retrieve remote file from '%s' !",
        url,
    )
    raise HttpClientError(url)

  def _create_request_session(self) -> Session:
    adapter = HTTPAdapter(max_retries=self.retry_config)
    session = Session()
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

  def _save_response(self, response: requests.Response, target: str) -> None:
    with open(
        target,
        'wb',
    ) as out_file:
      response.raw.decode_content = True
      shutil.copyfileobj(response.raw, out_file)
      self.log.info(f"HTTP GET: Successfully saved '{target}' !")
