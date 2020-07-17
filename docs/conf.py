#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The `configuration directory <https://www.sphinx-doc.org/en/master/glossary.html#term-configuration-directory>`_ must contain a file named ``conf.py``.

This file (containing Python code) is called the “build configuration file” and contains (almost) all configuration needed to customize Sphinx input and output behavior.

Notes
-----
An optional file `docutils.conf <http://docutils.sourceforge.net/docs/user/config.html>`_ can be added to
the configuration directory to adjust Docutils configuration if not otherwise overridden or set by Sphinx.


The configuration file is executed as Python code at build time
(using :func:`execfile`, and with the current directory set to its containing directory),
and therefore can execute arbitrarily complex code.
Sphinx then reads simple names from the file’s namespace as its configuration.

Important points to note:

    If not otherwise documented, values must be strings, and their default is the empty string.

    The term “fully-qualified name” refers to a string that names an importable Python object inside a module;
    for example, the FQN :code:`"sphinx.builders.Builder"` means the Builder class in the sphinx.builders module.

    Remember that document names use / as the path separator and don’t contain the file name extension.

    Since ``conf.py`` is read as a Python file, the usual rules apply for encodings and Unicode support.

    The contents of the config namespace are pickled (so that Sphinx can find out when configuration changes),
    so it may not contain unpickleable values – delete them from the namespace with del if appropriate.
    Modules are removed automatically, so you don’t need to del your imports after use.

    There is a special object named tags available in the config file.
    It can be used to query and change the tags (see `Including content based on tags <https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#tags>`_).
    Use :code:`tags.has('tag')` to query, :code:`tags.add('tag')` and :code:`tags.remove('tag')` to change.
    Only tags set via the :code:`-t` command-line option or via :code:`tags.add('tag')` can be queried using :code:`tags.has('tag')`.
    Note that the current builder tag is not available in ``conf.py``, as it is created after the builder is initialized.

"""  # noqa: E501

import os
import sys
import datetime

import assertionlib

sys.path.insert(0, os.path.abspath('..'))

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = '2.4'  # 2.0 or higher


# This value controls how to represents typehints. The setting takes the following values:
#     'signature' – Show typehints as its signature (default)
#     'none' – Do not show typehints
autodoc_typehints = 'signature'


# Output is processed with HTML4 writer.
# Default is False.
html4_writer = True


# Add any Sphinx extension module names here, as strings.
# They can be extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.duration',
    'sphinx.ext.doctest'
]


# Python code that is treated like it were put in a testsetup directive for
# every file that is tested, and for every group.
# You can use this to e.g. import modules you will always need in your doctests.
doctest_global_setup = """
from assertionlib.ndrepr import NUMPY_EX, PANDAS_EX
"""


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']


# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string: source_suffix = ['.rst', '.md']
source_suffix = '.rst'


# The master toctree document.
master_doc = 'index'


# General information about the project.
project = 'AssertionLib'
_year = str(datetime.datetime.now().year)
author = assertionlib.__author__
copyright = f'{_year}, {author}'


# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the built documents.
release = assertionlib.__version__  # The full version, including alpha/beta/rc tags.
version = release.rsplit('.', 1)[0]  # The short X.Y version.


# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'


# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store'
]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'


# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options: dict = {}


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory.
# They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
# This is required for the alabaster theme
# refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',  # needs 'show_related': True theme option to display
        'searchbox.html',
        'donate.html',
    ]
}


# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'assertionlib_doc'


# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc,
     f'{project}.tex',
     f'{project} Documentation',
     author,
     'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc,
     project,
     f'{project} Documentation',
     [author],
     1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc,
     project,
     f'{project} Documentation',
     author,
     'A package for performing assertions and providing informative exception messages.',
     'Miscellaneous'),
]


# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'pandas': ('https://pandas.pydata.org/pandas-docs/stable/', None),
    'numpy': ('https://docs.scipy.org/doc/numpy/', None),
    'plams': ('https://www.scm.com/doc/plams/', None)
}


# This value selects if automatically documented members are sorted alphabetical
# (value 'alphabetical'), by member type (value 'groupwise') or by source order
# (value 'bysource').
autodoc_member_order = 'bysource'


# True to parse NumPy style docstrings.
# False to disable support for NumPy style docstrings.
# Defaults to True.
napoleon_numpy_docstring = True


# True to parse NumPy style docstrings.
# False to disable support for NumPy style docstrings.
# Defaults to True.
napoleon_google_docstring = False


# True to use the .. admonition:: directive for the Example and Examples sections.
# False to use the .. rubric:: directive instead. One may look better than the other
# depending on what HTML theme is used.
# Defaults to False.
napoleon_use_admonition_for_examples = True


# True to use the .. admonition:: directive for Notes sections.
# False to use the .. rubric:: directive instead.
#  Defaults to False.
napoleon_use_admonition_for_notes = True


# True to use the .. admonition:: directive for References sections.
# False to use the .. rubric:: directive instead.
# Defaults to False.
napoleon_use_admonition_for_references = True


# A string of reStructuredText that will be included at the end of every source file that is read.
# This is a possible place to add substitutions that should be available
# in every file (another being rst_prolog).
rst_epilog = """
.. |plams.Settings| replace:: :class:`plams.Settings<scm.plams.core.settings.Settings>`
.. |plams.Molecule| replace:: :class:`plams.Molecule<scm.plams.mol.molecule.Molecule>`
.. |plams.Bond| replace:: :class:`plams.Bond<scm.plams.mol.bond.Bond>`
.. |plams.Atom| replace:: :class:`plams.Atom<scm.plams.mol.atom.Atom>`
"""
