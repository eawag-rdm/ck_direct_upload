# _*_ coding: utf-8 _*_

## Read arguments:
##    - server (default = 'https://data.eawag.ch'
##    - env. variable for apikey (default = CKAN_APIKEY_PROD1)
##    - path to source directory

## Read a directory. Record filenames and sizes. Read metadata.toml.
## Record attributes. Required:
##    - package_name

## Look for a package with specified name. Exit if it can't be found

## For each file check that there is none with the same name already present.
## Exit if there is.

## Calculate checksums for each file.

## Upload a dummy-file (same name, content is the name) for each ressource.

## Find the path on the file-system (TODO ssh, username, key?) for each ressource.
## Check whether it contains exactly what it should.
## If success: overwrite.

"""ck_direct_upload

Copies (large) files via scp from a SOURCEPATH to the ckan storage
path for resources on SERVER.

SOURCEPATH has to contain a file "direct_upload.toml". See the example
file in this program's distribution for documentation. The user of
this program needs passwordless ssh-access to SERVER and write
permissions for the CKAN storage path on that server.

Small dummy replacements for the files in SOURCEPATH are submitted
through the FileStore API. In a second step, the dummy-files on the
filesystem are replaced with the real files copied SOURCEPATH. All
resources need to be in SOURCEPATH, sub-directories are ignored.

Usage:
    ck_direct_upload [-s SERVER] [-p PKGNAME] [-a APIKEYVAR] SOURCEPATH
    ck_direct_upload -h

Options:
    --help -h       This help.

    -s SERVER       CKAN server. Overrides the specification in
                    PATH/direct_upload.toml (default: https://data.eawag.ch).

    -p PKGNAME      Name of the package. Overrides the specification in
                    PATH/direct_upload.toml. Must be specified somewhere.

    -a APIKEYVAR    Env. variable with API-key. Overrides the
                    specification in PATH/direct_upload.toml (default:
                    CKAN_APIKEY_PROD1).

Arguments:
    SOURCEPATH    Path to the source directory with ressources.

"""

from tomlkit import parse
from docopt import docopt
from ckanapi import RemoteCKAN, errors
import os.path
import io

defaultconfig = {
    'SERVER': 'https://data.eawag.ch',
    'APIKEYVAR': 'CKAN_APIKEY_PROD1'}


configfilename = 'direct_upload.toml'


def _getargs(args):
    arga = docopt(__doc__, argv=args)
    return arga


def _readconfig(path, fn=configfilename):
    with open(os.path.join(path, fn), 'r') as f:
        config = parse(f.read())
    return config


def buildconfig(args):
    # map docopt <-> configfile parameters
    m = {'-s': 'SERVER', '-a': 'APIKEYVAR', '-p': 'PKGNAME',
         'SOURCEPATH':'SOURCEPATH'}
    cliargs = _getargs(args)
    config = {m[k]: v for (k, v) in cliargs.items() if k != '--help'}
    
    try:
        configfileargs = _readconfig(config['SOURCEPATH'])
    except FileNotFoundError:
        pass
    else:
        config.update({k: configfileargs.get(k) for (k, v) in config.items()
                       if v is None})
        
    config.update({k: defaultconfig.get(k) for (k, v) in config.items()
                   if v is None})
    if None in config.values():
        print('No package-name given. Exiting.')
        raise SystemExit
                
    return config


def readsource(path):
    if not os.path.isdir(path):
        raise ValueError('Source directory "{}" not found'.format(path))

    filenames = [fn for fn in os.listdir(path) if fn != configfilename]
    if not filenames:
        print('The source directory {} is empty. Exiting.'.format(path))
        raise(SystemExit)
    
    fileinfo = {fn: os.path.getsize(os.path.join(path, fn)) for fn in filenames}
    return fileinfo


def _get_conn(config):
    return RemoteCKAN(config['SERVER'], os.environ[config['APIKEYVAR']])


def getpackage(conn, config):
    try:
        res = conn.call_action('package_show', {'id': config['PKGNAME']})
    except errors.NotFound:
        print('The package with the name "{}" doesn\'t exist on {}. Exiting'
              .format(config['PKGNAME'], config['SERVER']))
        raise ValueError
    return res
    
                    
    
# next:  check pkg has (no resources or one resorce called "dummy")


    
              
