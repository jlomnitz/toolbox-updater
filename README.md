# README #

This is part of the Design Space Toolbox V2 project, a software implementation of the System Design Space method developed by Jason G. Lomnitz, originally developed in the laboratory of Michael A. Savageau. This method decomposes complex nonlinear systems into a finite number of tractable nonlinear subsystems.

### What is this repository for? ###

Installation script for the Design Space Toolbox C library (libdesignspace) and its Python interface (dspace package). This script updates the repositories through git and identifies the latest version. By default the script downloads the most recent release version.

### How do I get set up? ###

To install, type in the following commands in a terminal window:

    cd
    curl https://bitbucket.org/jglomnitz/toolbox-update-script/raw/v1.2.0/toolbox_update.py -O
    chmod +x toolbox_update.py

To update the script (recommended after install):

    ./toolbox_update.py --update-script

This script updates the Design Space V2 C toolbox and Python package.

The C toolbox has dependencies on the following libraries (`stable` and `release` indicate the dependencies of the stable and release version of the C toolbox):

1. libgsl `stable` `release`
2. libprotobuf `stable`
3. libprotobuf-c (> v1.0.0) `stable`
4. libglpk (modified for parallel analysis of multiple linear programming problems) `stable` `release`

Libraries (1)-(3) must be installed by the user. The modified version of the GLPK is automatically installed by this script by adding the `--glpk-dependency` flag during installation of the library.

The Python interface requires Python 2.7.x. The Python Interface provides plotting utilities that are added to the base package by importing the dspace.plotutils package that has the folliwing dependencies:

1. NumPy
2. SciPy
3. Matplotlib

If the included plotting utilities are not required, these dependencies need not be installed.

### Initial Install of Design Space Toolbox V2 to the latest version ###

To install, one must first have access to the C library repository and it must be cloned [default location is ~/Documents/design-space-c-toolbox].

Once the repository is cloned, first time installation of the library should use the following command,

    sudo ./toolbox_update.py --stable --glpk-dependency

which instructs the update script to download and install a modified version of the GNU Linear Programming Kit, a dependency, that supports analysis of multiple linear programming problems in parallel.  The update script build the most recent stable version of the toolbox, which is recommended over the current release version. Alternatively, one may install the latest release version through the following command,

    sudo ./toolbox_update.py --release --glpk-dependency


### Updating the toolbox ###


To update these packages to the latest release versions:

    sudo ./toolbox_update.py --release

For the stable development version:

    sudo ./toolbox_update.py --stable

For more information, refer to the help page:

    ./toolbox_update.py -h

### Who do I talk to? ###

Any questions, please contact Jason Lomnitz via e-mail (jlomn AT ucdavis.edu), with "DSTV2 Q:" as the subject prefix.