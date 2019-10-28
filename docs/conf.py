#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# qmflows documentation build configuration file, created by
# sphinx-quickstart on Wed Nov  8 12:07:40 2017.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys
import datetime

import assertionlib

sys.path.insert(0, os.path.abspath('..'))

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = '2.0'  # 2.0 or higher


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
    # 'sphinx_autodoc_typehints'  # ?????? AttributeError: 'function' object has no attribute '<locals>'
]


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']


# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string: source_suffix = ['.rst', '.md']
source_suffix = '.rst'


# The master toctree document.
master_doc = 'index'


# General information about the project.
project = 'AssertionLib'
year = str(datetime.datetime.now().year)
author = assertionlib.__author__
copyright = f'{year}, {author}'


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
#
# html_theme_options = {}

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


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}




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


# This value selects if automatically documented members are sorted alphabetical (value 'alphabetical'),
# by member type (value 'groupwise') or by source order (value 'bysource').
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
# False to use the .. rubric:: directive instead. One may look better than the other depending on what HTML theme is used.
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
# This is a possible place to add substitutions that should be available in every file (another being rst_prolog).
rst_epilog = """
.. |plams.Settings| replace:: :class:`plams.Molecule<scm.plams.core.settings.Settings>`
.. |plams.Molecule| replace:: :class:`plams.Molecule<scm.plams.mol.molecule.Molecule>`
.. |plams.Bond| replace:: :class:`plams.Bond<scm.plams.mol.bond.Bond>`
.. |plams.Atom| replace:: :class:`plams.Atom<scm.plams.mol.atom.Atom>`
"""
