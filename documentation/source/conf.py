"""Configuration file for the Sphinx documentation builder."""
# pylint: disable=invalid-name

# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

import os
import pathlib
import sys

os.environ["SPHINX"] = "1"

if os.path.exists('/app'):
  sys.path.insert(0, os.path.abspath('/app'))
if os.path.exists('../../pi_portal'):
  sys.path.insert(0, os.path.abspath('../..'))
  sys.path.insert(0, os.path.abspath('../../pi_portal'))

# -- Project information -----------------------------------------------------
project = 'pi_portal'
author = 'Niall Byrne'
os.environ['PROJECT_NAME'] = project

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinx-jsonschema',
    'sphinx_click',
    'myst_parser',
]


def autosummary_filter():
  """Create a list of import paths to exclude from documentation."""
  exclude_paths = []
  project_dir = os.path.join("..", "..", project)
  for root, dirs, filenames in os.walk(project_dir):
    root = pathlib.Path(root).relative_to(os.path.join("..", ".."))

    for name in set(dirs).intersection(autosummary_filter_folders):
      exclude_path = root / name
      exclude_paths.append('.'.join(exclude_path.with_suffix('').parts))

    for filename in set(filenames).intersection(autosummary_filter_filenames):
      exclude_path = root / os.path.splitext(filename)[0]
      exclude_paths.append('.'.join(exclude_path.with_suffix('').parts))

  return exclude_paths


autosummary_filter_folders = {"__pycache__", "tests"}
autosummary_filter_filenames = {"conftest.py"}
autosummary_mock_imports = autosummary_filter()

source_suffix = {
    '.rst': 'restructuredtext',
}

always_document_param_types = False

autosummary_generate = True
autodoc_typehints = "both"
autodoc_typehints_format = "short"
autodoc_inherit_docstrings = True
autodoc_typehints_description_target = "documented_params"

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_css_files = [
    'css/overrides.css',
]
