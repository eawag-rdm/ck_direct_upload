# _*_ coding: utf-8 _*_

## Read arguments:
##    - server (default = 'https://data.eawag.ch'
##    - env. variable for apikey (default = CKAN_APIKEY_PROD1)
##    - path to source directory

## Read a directory. Record filenames and sizes. Read metadata.toml.
## Record attributes. Required:
##    - package_name
##    - "resource_type". Default: "Dataset".

## Look for a package with specified name. Exit if it can't be found

## For each file check that there is none with the same name already present.
## Exit if there is.

## Calculate checksums for each file.

## Upload a dummy-file (same name, content is the name) for each ressource.

## Find the path on the file-system (TODO ssh, username, key?) for each ressource.
## Check whether it contains exactly what it should.
## If success: overwrite.

"""ck_direct_upload

Usage:
    ck_direct_upload [-s SERVER] [-a APIKEYVAR] PATH
    ck_direct_upload -h

Options:
    --help -h       This help.
    -s SERVER       Server [default: https://data.eawag.ch]
    -a APIKEYVAR    Env. variable with API-key [default: CKAN_APIKEY_PROD1]

Arguments:
    PATH    Path to the source diretory with ressources.

"""

from docopt import docopt
import os.path


def getargs(args):
    arga = docopt(__doc__, argv=args)
    return arga

def readsource(path):
    if not os.path.isdir(path):
        raise ValueError('Source directory "{}" not found'.format(path))
    ## Exit if no toml file or no package specified in toml.
    
    
