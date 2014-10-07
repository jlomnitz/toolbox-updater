#!/usr/bin/python

from subprocess import call, Popen, PIPE
from distutils.version import StrictVersion
import argparse
import os
from os import path

__version__ = '0.2.0'

STABLE_VERSION='develop'

DEFAULT_TOOLBOX_VERSION = '$RELEASE'
DEFAULT_INTERFACE_VERSION = '$RELEASE'

DESCRIPTION_STRING = \
''' Script to update the Design Space Toolbox V2 and its
python interface. The script switches to the appropriate branch and 
pulls from origin and runs make/xcodebuild to install depending on 
linux/mac system. The command builds the latest release as default.'''

def parse_arguments(): 
    parser = argparse.ArgumentParser(prog='Design space toolbox and interface updater',
                                     description=DESCRIPTION_STRING)
    parser.add_argument('--stable', dest='stable_or_release', action='store_const',
                        const='stable',
                        help='build latest stable version')
    parser.add_argument('--release', dest='stable_or_release', action='store_const',
                        const='release', default='release',
                        help='build latest release version')
    parser.add_argument('--toolbox_version', dest='toolbox_version',
                        default=DEFAULT_TOOLBOX_VERSION, 
                        type=str,
                        help='build a specific version or branch of the c library')
    parser.add_argument('--interface_version', dest='interface_version',
                        default=DEFAULT_INTERFACE_VERSION, 
                        type=str,
                        help='build a specific version or branch of the python interface')
    parser.add_argument('--linux', dest='is_linux', action='store_true',
                        help='indicates if it should build using linux commands')
    parser.add_argument('--toolbox_dict', dest='toolbox_dict', 
                        default='~/Documents/design-space-toolbox/',
                        type=str,
                        help='directory for the c toolbox local git repository')
    parser.add_argument('--interface_dict', dest='interface_dict', 
                        default='~/Documents/python-design-space-interface/', 
                        type=str,
                        help='directory for the c toolbox local git repository')
    args = parser.parse_args()
    return args

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
       
def update_c_toolbox(args):
    pwd = os.getcwd()
    os.chdir(path.expanduser(args.toolbox_dict))
    call(['git', 'fetch', '--all'])
    version = args.toolbox_version
    if version == '$RELEASE':
        version=get_latest_release()
    if args.stable_or_release == 'release':
        version=get_latest_release()
    if args.stable_or_release == 'stable':
        version=STABLE_VERSION
    versions = get_release_versions()
    if version not in versions:
        versions = get_remote_branches()
        version = 'origin/'+version
        if version not in versions:
            raise ValueError, 'selected version of toolbox does not exist'
            return 1
    else:
        version = 'tags/'+version
    print 'Building ' + version.split('/')[1]
    call(['git', 'checkout', version])
    if args.is_linux is True:
        call(['sudo', 'make', 'install'])
    else:
        call(['xcodebuild'])
        call(['sudo', 'cp'] + os.listdir('build/Release/usr/local/include/') + ['/usr/local/include/designspace/'])
        call(['sudo', 'cp', 'build/Release/libdesignspace.dylib', '/usr/local/lib/'])
    os.chdir(pwd)
    return 0

def update_python_interface(args):
    pwd = os.getcwd()
    os.chdir(path.expanduser(args.interface_dict))
    call(['git', 'fetch', '--all'])
    version = args.interface_version
    if version == '$RELEASE':
        version=get_latest_release()
    if args.stable_or_release == 'release':
        version=get_latest_release()
    if args.stable_or_release == 'stable':
        version=STABLE_VERSION
    versions = get_release_versions()
    if version not in versions:
        versions = get_remote_branches()
        version = 'origin/'+version
        if version not in versions:
            raise ValueError, 'selected version of toolbox does not exist'
            return 1
    else:
        version = 'tags/'+version
    print 'Building ' + version.split('/')[1]
    call(['git', 'checkout', version])
    call(['sudo', 'python', 'setup.py', 'install'])
    os.chdir(pwd)
    return 0
        
if __name__ == '__main__':
    args=parse_arguments()
    print args
    update_c_toolbox(args)
    update_python_interface(args)
