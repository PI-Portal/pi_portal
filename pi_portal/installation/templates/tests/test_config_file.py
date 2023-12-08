"""Test the ConfileFileTemplate class."""

from contextlib import closing
from io import StringIO
from unittest import mock

from pi_portal import config
from pi_portal.modules.configuration import state
from .. import config_file

CONFIG_FILE_MODULE = config_file.__name__


class TestConfigFileTemplate:
  """Test the ConfileFileTemplate class."""

  def test__initialize__attrs(
      self,
      config_file_template: config_file.ConfileFileTemplate,
      source_file: str,
      destination_file: str,
  ) -> None:

    assert config_file_template.source == source_file
    assert config_file_template.destination == destination_file

  def test__create_context__returns_dict(
      self,
      mocked_state: state.State,
      config_file_template: config_file.ConfileFileTemplate,
  ) -> None:
    expected_values = {
        "LOGZ_IO_CODE": mocked_state.user_config["LOGZ_IO_CODE"],
    }
    for setting in dir(config):
      if not setting.startswith("__"):
        expected_values[setting] = getattr(config, setting)

    result = config_file_template.create_context()

    assert result == expected_values

  @mock.patch(CONFIG_FILE_MODULE + ".JinjaTemplate")
  @mock.patch(CONFIG_FILE_MODULE + ".open")
  def test__render__file_transactions(
      self,
      m_open: mock.Mock,
      m_template: mock.Mock,
      config_file_template: config_file.ConfileFileTemplate,
  ) -> None:
    m_template.return_value.render.return_value = "rendered template"
    mock_source = StringIO("template")
    mock_destination = mock.Mock()
    m_open.side_effect = [closing(mock_source), closing(mock_destination)]

    config_file_template.render()

    assert m_open.mock_calls == \
        [
            mock.call(config_file_template.source, 'r', encoding='utf-8'),
            mock.call(config_file_template.destination, 'w', encoding='utf-8'),
        ]
    mock_destination.write.assert_called_once_with("rendered template")

  @mock.patch(CONFIG_FILE_MODULE + ".JinjaTemplate")
  @mock.patch(CONFIG_FILE_MODULE + ".open", mock.mock_open())
  def test__render__template_rendered(
      self,
      m_template: mock.Mock,
      config_file_template: config_file.ConfileFileTemplate,
  ) -> None:
    m_template.return_value.render.return_value = "rendered template"

    config_file_template.render()

    m_template.return_value.render.assert_called_once_with(
        config_file_template.create_context()
    )
