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
      mocked_source_file: str,
      mocked_destination_file: str,
  ) -> None:
    assert config_file_template.context == {}
    assert config_file_template.source == mocked_source_file
    assert config_file_template.destination == mocked_destination_file

  def test__update_context__stores_updated_context(
      self,
      test_state: state.State,
      config_file_template: config_file.ConfileFileTemplate,
  ) -> None:
    expected_values = {
        "USER_CONFIG": test_state.user_config,
    }
    for setting in dir(config):
      if not setting.startswith("__"):
        expected_values[setting] = getattr(config, setting)

    config_file_template.update_context()

    assert config_file_template.context == expected_values

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
        config_file_template.context
    )
