# add package path
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

# project details
project = 'llmbox'
copyright = '2023, Victory Crest'
author = 'Victory Crest'
release = '0.1.0'

# install extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon'
]

# configure rtd
templates_path = ['_templates']
exclude_patterns = []
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
add_module_names = False

# configure autodoc
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'member-order': 'bysource'
}
