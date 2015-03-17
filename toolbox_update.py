#!/usr/bin/python
'''
Design Space Toolbox Update Script

Copyright (C) 2014 Jason G. Lomnitz.

The Design Space Toolbox Update Script is free software: you can redistribute it 
and/or modify it under the terms of the GNU General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

The Design Space Toolbox Update Script is distributed in the hope that it will
be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with the Design Space Toolbox Update Script. If not, see 
<http://www.gnu.org/licenses/>.
'''


from subprocess import call, Popen, PIPE
from distutils.version import StrictVersion
import sys
import argparse
import os
from os import path


## dependency_checks = {'

__version__ = '1.4.0a1'

# Temporarly uses the develop-0.3.0 branch. In the future, this will be
# changed back to develop and develop-0.3.0 will be deleted.
STABLE_VERSION='develop'

# Default behavior is to download latest release version.
# Special variables are $RELEASE and $STABLE.
DEFAULT_TOOLBOX_VERSION = '$RELEASE'
DEFAULT_INTERFACE_VERSION = '$RELEASE'

DESCRIPTION_STRING = \
''' Script to update the Design Space Toolbox V2 and the Design Space
Python Interface. The script switches to the appropriate branch and 
pulls from origin and installs the packages on the either Mac OS X or 
linux systems. This script does not install any dependencies.
Executing the script without any options builds the latest release version.
Current stable version of the toolbox is 'develop'.'''

def parse_arguments(): 
    parser = argparse.ArgumentParser(prog='toolbox_update',
                                     description=DESCRIPTION_STRING)
    parser.add_argument('--version', dest='print_version', action='store_true',
                        help='print script version')
    parser.add_argument('-v', dest='verbose_mode', action='store_true',
                        help='run program in verbose mode (does not install, show available versions)')
    parser.add_argument('-B', '--Build-dir', dest='build_dir',
                        default='~/.DSTV2_INSTALL',
                        help='indicates the toolbox build directory')
    parser.add_argument('-s', '--stable', dest='stable_or_release', action='store_const',
                        const='stable',
                        help='build latest stable version')
    parser.add_argument('-r', '--release', dest='stable_or_release', action='store_const',
                        const='release', default='release',
                        help='build latest release version')
    parser.add_argument('-t', '--toolbox-version', dest='toolbox_version',
                        default=DEFAULT_TOOLBOX_VERSION, 
                        type=str,
                        help='build a specific version or branch of the c library')
    parser.add_argument('-i', '--interface-version', dest='interface_version',
                        default=DEFAULT_INTERFACE_VERSION, 
                        type=str,
                        help='build a specific version or branch of the python interface')
    parser.add_argument('-u', '--update-script', dest='self_update', action='store_true',
                        help='update this script')
    parser.add_argument('-T', '--toolbox-dir', dest='toolbox_dict', 
                        default='~/Documents/design-space-toolbox/',
                        type=str,
                        help='directory for the c toolbox local git repository')
    parser.add_argument('-I', '--interface-dir', dest='interface_dir', 
                        default='python-design-space-interface', 
                        type=str,
                        help='directory for the c toolbox local git repository')
    parser.add_argument('-G', '--glpk-dir', dest='glpk_dir', 
                        default='glpk-with-thread-specific-env', 
                        type=str,
                        help='directory for the c toolbox local git repository')
    parser.add_argument('--only-toolbox', dest='single', action='store_const',
                        const='toolbox',
                        help='only update the c library')
    parser.add_argument('--only-interface', dest='single', action='store_const',
                        const='interface',
                        help='only update the python interface')
    parser.add_argument('--no-fetch', dest='no_update', action='store_true',
                        help='indicates if it should switch without downloading from server')
    parser.add_argument('--restore-old', dest='restore', action='store_true',
                        help='indicates if it should switch without downloading from server')
    parser.add_argument('--glpk-dependency', dest='glpk_dep', action='store_true',
                        help='indicates if it should install glpk dependency')
    args = parser.parse_args()
    return args

def c_toolbox_version():
    cmd = Popen(['grep', '__DS_DESIGN_SPACE_VERSION__', 'DSTypes.h'], stdout=PIPE, stderr=PIPE)
    out, err = cmd.communicate()
    
def get_latest_release():
    versions = get_release_versions()
    strict = [StrictVersion(i[1:]) for i in versions]
    maxVersion = max(strict)
    return versions[strict.index(maxVersion)]
    
def get_release_versions():
    cmd = Popen(['git', 'tag'], stdout=PIPE)
    out, err = cmd.communicate()
    return out.splitlines()

def get_branches():
    cmd = Popen(['git', 'branch'], stdout=PIPE)
    out, err = cmd.communicate()
    branches = out.splitlines()
    branches = [i.split(' ')[-1] for i in branches]
    return branches
 
def get_remote_branches():
    cmd = Popen(['git', 'branch', '-r'], stdout=PIPE)
    out, err = cmd.communicate()
    remote = out.splitlines()
    remote = [i.strip() for i in remote]
    return remote
       
def install_custom_glpk(args):
    pwd = os.getcwd()
    os.chdir(path.expanduser(args.build_dir))
    dirs = os.listdir(path.expanduser(args.build_dir))
    if args.glpk_dir not in dirs:
        call(['git',
              'clone', 
              'https://jglomnitz@bitbucket.org/jglomnitz/glpk-with-thread-specific-env.git', 
              args.glpk_dir])
    os.chdir(args.glpk_dir)
    call(['git', 'pull', 'origin', 'master'])
    print 'Configuring GLPK (modified for pthread) using make...'
    cmd = Popen(['./configure'], stdout=PIPE, stderr=PIPE)
    out, err = cmd.communicate()
    p = Popen(['grep', 'error'], stdin=PIPE)
    p.communicate(input=out)
    p = Popen(['grep', 'error'], stdin=PIPE)
    p.communicate(input=err)
    print 'Building GLPK (modified for pthread) using make...'
    cmd = Popen(['make', 'install'], stdout=PIPE, stderr=PIPE)
    out, err = cmd.communicate()
    p = Popen(['grep', 'error'], stdin=PIPE)
    p.communicate(input=out)
    p = Popen(['grep', 'error'], stdin=PIPE)
    p.communicate(input=err)


def update_c_toolbox(args):
    pwd = os.getcwd()
    os.chdir(path.expanduser(args.toolbox_dict))
    version = args.toolbox_version
    if version == '$RELEASE':
        version=get_latest_release()[1:]
    if version == '$STABLE':
        version = STABLE_VERSION
    if args.stable_or_release == 'release':
        version=get_latest_release()[1:]
    if args.stable_or_release == 'stable':
        version=STABLE_VERSION
    versions = get_release_versions()
    if 'v'+version not in versions:
        versions = get_remote_branches()
        version = 'origin/'+version
        if version not in versions:
            raise ValueError, 'selected version of toolbox does not exist'
            return 1
    else:
        version = 'tags/v'+version
    result = ''
    while 1:
        result = raw_input('Build C toolbox version ' + version.split('/')[1] + '?[Y/n]')
        if result.lower() in ['y', 'n', '']:
            break
        print "'" + result + "' is not a valid response."
    if result.lower() == 'n':
        return 0     
    call(['git', 'checkout', version])
    if args.use_make is True:
        ## call(['make', 'install'])
        print 'Building using make...'
        cmd = Popen(['make', 'install'], stdout=PIPE, stderr=PIPE)
        out, err = cmd.communicate()
        p = Popen(['grep', 'error'], stdin=PIPE)
        p.communicate(input=out)
        p = Popen(['grep', 'error'], stdin=PIPE)
        p.communicate(input=err)
    else:
        print 'Building using xcodebuild...'
        cmd = Popen(['xcodebuild'], stdout=PIPE, stderr=PIPE)
        out, err = cmd.communicate()
        p = Popen(['grep', 'error'], stdin=PIPE)
        p.communicate(input=out)
        p = Popen(['grep', 'error'], stdin=PIPE)
        p.communicate(input=err)
        print 'Installing...'
        call(['cp'] + os.listdir('build/Release/usr/local/include/') + ['/usr/local/include/designspace/'])
        call(['cp', 'build/Release/libdesignspace.dylib', '/usr/local/lib/'])
        print 'Done'
    os.chdir(pwd)
    return 0

def update_python_interface(args):
    pwd = os.getcwd()
    os.chdir(path.expanduser(args.build_dir))
    os.chdir(args.interface_dir)
    version = args.interface_version
    if version == '$RELEASE':
        version=get_latest_release()[1:]
    if version == '$STABLE':
        version = STABLE_VERSION
    if args.stable_or_release == 'release':
        version=get_latest_release()[1:]
    if args.stable_or_release == 'stable':
        version=STABLE_VERSION
    versions = get_release_versions()
    if 'v'+version not in versions:
        versions = get_remote_branches()
        version = 'origin/'+version
        if version not in versions:
            raise ValueError, 'selected version of toolbox does not exist'
            return 1
    else:
        version = 'tags/v'+version
    result = ''
    while 1:
        result = raw_input('Build Python Interface version ' + version.split('/')[1] + '?[Y/n]')
        if result.lower() in ['y', 'n', '']:
            break
        print "'" + result + "' is not a valid response."
    if result.lower() == 'n':
        return 0     
    call(['git', 'checkout', version])
    call(['python', 'setup.py', 'install'])
    os.chdir(pwd)
    return 0
    
def update_repositories(args):
    if args.no_update is False:
        pwd = os.getcwd()
        os.chdir(path.expanduser(args.toolbox_dict))
        call(['git', 'fetch', '--all'])
        os.chdir(path.expanduser(args.build_dir))
        dirs = os.listdir(path.expanduser(args.build_dir))
        if args.interface_dir not in dirs:
            print 'Creating ' + args.interface_dir + ' at ' + os.chdir(path.expanduser(args.build_dir))
            call(['git',
                  'clone', 
                  'https://jglomnitz@bitbucket.org/jglomnitz/python-design-space-interface.git', 
                  args.interface_dir])
        os.chdir(args.interface_dir)
        call(['git', 'fetch', '--all'])
        os.chdir(pwd)
    return

def verbose_mode_fn(args, directory):
    global STABLE_VERSION
    pwd = os.getcwd()
    os.chdir(path.expanduser(directory))
    print 'Release versions:'
    versions = get_release_versions()
    release = get_latest_release()
    for version in versions:
        if version == release:
            current = ' * '
        else:
            current = '   '
        current += version[1:]
        print current
    print 'Development versions:'
    versions = get_remote_branches()
    stable = STABLE_VERSION
    for version in versions:
        version = version.split('/')[1]
        if version == master:
            continue
        if version == stable:
            current = ' * '
        else:
            current = '   '
        current += version
        print current
    os.chdir(pwd)
    
def verbose_mode(args):
    global DESCRIPTION_STRING
    global __version__
    print 'toolbox_update.py   ' +  __version__
    print DESCRIPTION_STRING
    print ''
    print 'C toolbox:' 
    print '----------'   
    verbose_mode_fn(args, args.toolbox_dict)
    print 'Python interface:'
    print '-----------------'   
    verbose_mode_fn(args, args.interface_dict)
    
    
def update_script(args):
    global __version__
    call(['curl',
          'https://bitbucket.org/jglomnitz/toolbox-update-script/raw/develop/toolbox_update.py',
          '-o',
          'toolbox_update_temp.py'])
    result = ''
    try:
        from toolbox_update_temp import __version__ as new_version
    except:
        print 'Cannot compile new version of toolbox. Aborting.'
        return
    while 1:
        result = raw_input('Update script '+__version__+'->'+new_version+'?[Y/n]')
        if result.lower() in ['y', 'n', '']:
            break
        print "'" + result + "' is not a valid response."
    if result.lower() == 'n':
        call(['rm', 'toolbox_update.py.temp'])
        return 0 
    call(['mv', 'toolbox_update.py', 'toolbox_update.py.old'])
    call(['mv', 'toolbox_update_temp.py', 'toolbox_update.py'])
    call(['chmod', '+x', 'toolbox_update.py'])
    return

def restore_old(args):
    global __version__
    result = ''
    while 1:
        result = raw_input('Restore to previous script?[Y/n]')
        if result.lower() in ['y', 'n', '']:
            break
        print "'" + result + "' is not a valid response."
    if result.lower() == 'n':
        return 0 
    call(['mv', 'toolbox_update.py.old', 'toolbox_update.py'])
    call(['chmod', '+x', 'toolbox_update.py'])
    return

def __main__(args):
    call(['mkdir', '-p', path.expanduser(args.build_dir)])
    if args.print_version is True:
        print 'Toolbox Update Script '+ __version__
        return
    if args.self_update is True:
        update_script(args)
        return
    if args.restore is True:
        restore_old(args)
        return
    update_repositories(args)
    if args.verbose_mode is True:
        verbose_mode(args)
        return
    if sys.platform.startswith('darwin'):
        args.use_make = False
    else:
        args.use_make = True
    if args.glpk_dep == True:
        install_custom_glpk(args)
    if args.single != 'interface':
        update_c_toolbox(args)
    if args.single != 'toolbox':
        update_python_interface(args)

if __name__ == '__main__':
    args=parse_arguments()
    __main__(args)
    
    
    
    
