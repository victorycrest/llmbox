import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

project = 'llmbox'
copyright = '2023, Victory Crest'
author = 'Victory Crest'
release = '0.1.0'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon'
]
templates_path = ['_templates']
exclude_patterns = []
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
add_module_names = False
