# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join("..", "..")))


# -- Project information -----------------------------------------------------
master_doc = "index"
project = 'rebalance'
copyright = '2020, Siavosh Shadpey'
author = 'Siavosh Shadpey'

# The full version, including alpha/beta/rc tags
release = '0.0.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.mathjax",
    "sphinx.ext.intersphinx",
    "numpydoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.napoleon",
]

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = False

todo_include_todos = False

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

autodoc_mock_imports = ['forex_python', 'yfinance', 'numpy', 'scipy', 'typing']
autodoc_default_flags = ['members', 'private-members', 'special-members', 'inherited-members', 'show-inheritance']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme_path = ["."]
html_theme = "semantic_sphinx"
html_theme_options = {
    "navbar_links": [
        ("Documentation", "documentation"),
    #    ("Examples", "nb_examples/index"),
    #    ("Books + Videos", "learn"),
    #    ("API", "api"),
    #    ("Developer Guide", "developer_guide"),
    #    ("About PyMC3", "history")
    ],
    #     "fixed_sidebar": "false",
    #     "description": "Probabilistic Programming in Python: Bayesian Modeling and Probabilistic Machine Learning with Theano"
}
html_sidebars = {"**": ["about.html", "navigation.html", "searchbox.html"]}

source_suffix = ['.rst', '.md']

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "friendly"


def setup(app):
    app.add_css_file(
        "https://cdn.jsdelivr.net/npm/semantic-ui@2.4.2/dist/semantic.min.css"
    )
    app.add_css_file("default.css")