# README #

### What is this repository for? ###

Installation script for the Design Space Toolbox C library (libdesignspace) and its Python interface (dspace package). This script updates the repositories through git and identifies the latest version. By default the script downloads the most recent release version.

### How do I get set up? ###

To install type in the following commands in a terminal window:

    cd
    curl https://bitbucket.org/jglomnitz/toolbox-update-script/raw/v1.2.0/toolbox_update.py -O
    chmod +x toolbox_update.py

To update (recommended after install):

    ./toolbox_update.py --update-script

To update a pre-installed version of the C toolbox and Python package to latest release version:

    sudo ./toolbox_update.py --release

For the stable development version:

    sudo ./toolbox_update.py --stable

### Who do I talk to? ###

Any questions please email: Jason Lomnitz (jlomn@ucdavis.edu)