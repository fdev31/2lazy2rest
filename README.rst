##########
2lazy2rest
##########

A simple way to produce short-to-medium document using *reStructuredText*

Multi-format themes
    Render the same document in HTML, ODT, PDF keeping the main visual identity
Unified interface
    - Tired of switching between rst2* tools having different arguments or behavior ?
    - Would like to not lose *code-blocks* or some rendering options switching the output format ?

    This tool try to address this
Make your own theme
    TODO: templates will be customizable easily (say, probably colors only)

How to use it
#############

Dependencies
============

You'll need **rst2pdf** to use all the features, other rst2* tools are coming from docutils.

Using
=====

.. code-block:: console

    mkrst [-h] [--html] [--pdf] [--odt] [--theme THEME]
                 [--themes-dir THEMES_DIR]
                 FILE

optional arguments:
  -h, --help            show this help message and exit
  --html                Generate HTML output
  --pdf                 Generate PDF output
  --odt                 Generate ODT output
  --theme THEME         Use a different theme
  --themes-dir THEMES_DIR
                        Change the folder searched for theme


.. code-block:: console

    popo:~/2lazy2rest% ./mkrst test_page.rst --html --pdf
    Using ./themes/default
      html:  test_page.html
       pdf:  test_page.pdf


Customizing
===========

Make a copy of ``themes/default``, edit to your needs the copy and use the **--theme** option with the name of your copy, that's All !

Example
-------

.. code-block:: console

   popo:~/2lazy2rest% cp -r themes/default themes/red
   popo:~/2lazy2rest% sed -si 's/#FEFEFE/red/g' themes/red/html/stylesheet.css
   popo:~/2lazy2rest% ./mkrst test_page.rst --html --theme red

Issues
######

- ODT style is unfinished
- PDF & HTML still needs more ReST coverage
- No skin generation from template yet

