# README #

### What is this repository for? ###

Installation script for the Design Space Toolbox C library (libdesignspace) and its Python interface (dspace package). This script updates the repositories through git and identifies the latest version. By default the script downloads the most recent release version.

### How do I get set up? ###

To install type in the following commands in a terminal window:

    cd
    curl https://bitbucket.org/jglomnitz/toolbox-update-script/raw/v1.2.0/toolbox_update.py -O
    chmod +x toolbox_update.py

To update the script (recommended after install):

    ./toolbox_update.py --update-script

This script updates the Design Space V2 C toolbox and Python package. It requires git access to these repositories [direct requests for access to these repositories to Jason Lomnitz (jlomn@ucdavis.edu)].

To update these packages to the latest release versions:

    sudo ./toolbox_update.py --release

For the stable development version:

    sudo ./toolbox_update.py --stable

For more information, refer to the help page:

    ./toolbox_update.py -h


### Who do I talk to? ###

Any questions please email: Jason Lomnitz (jlomn@ucdavis.edu)