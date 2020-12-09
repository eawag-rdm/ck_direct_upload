import pytest as pt
import ck_direct_upload as du
import pathlib
import os


THISDIR = pathlib.Path(__file__).parent.absolute()

# paths relative to this file'sdirectory
TESTSOURCE = os.path.join(str(THISDIR), 'data')
TESTSOURCE_LARGE = os.path.join(str(THISDIR), 'data/largefiles/')
TESTSOURCE_EMPTY = os.path.join(str(THISDIR), 'data/empty/')


def test__getargs():
    with pt.raises(SystemExit):
        res = du._getargs(["-h"])
    res = du._getargs(['/the/path/to/hell','-a', 'keyenv', '-p', 'testpkgname',
                       '-s', 'somehost'])
    assert(res['--help'] is False
           and res['-s'] == 'somehost'
           and res['-a'] == 'keyenv'
           and res['SOURCEPATH'] == '/the/path/to/hell'
           and res['-p'] == 'testpkgname')
    res = du._getargs(['/the/path/to/hell'])
    assert(res['--help'] is False
           and res['-s'] is None and res['-a'] is None)

    
def test__readconfig():
    res = du._readconfig(TESTSOURCE)
    assert(res == {'APIKEYVAR': 'TEST_CKAN_APIKEY',
                   'SERVER': 'http://localhost:5000',
                   'PKGNAME': 'test_pkgname'})


def test_buildconfig():
    # just configfile
    conf = du.buildconfig([TESTSOURCE])
    assert(
        conf == {'SOURCEPATH': TESTSOURCE,
                 'SERVER': 'http://localhost:5000',
                 'APIKEYVAR': 'TEST_CKAN_APIKEY',
                 'PKGNAME': 'test_pkgname'})

    # Both default
    conf =  du.buildconfig(['-p', 'PackName', TESTSOURCE_EMPTY])
    assert(
        conf == {'SOURCEPATH': TESTSOURCE_EMPTY,
                 'SERVER': 'https://data.eawag.ch',
                 'APIKEYVAR': 'CKAN_APIKEY_PROD1',
                 'PKGNAME': 'PackName'})

    # SERVER: CLI, APIKEY: default    
    conf =  du.buildconfig(['-p', 'Packname', '-s', 'testserver',
                            TESTSOURCE_EMPTY])
    assert(
        conf == {'SOURCEPATH': TESTSOURCE_EMPTY,
                 'SERVER': 'testserver',
                 'APIKEYVAR': 'CKAN_APIKEY_PROD1',
                 'PKGNAME': 'Packname'})

    # SERVER: default,  APIKEY: configfile
    conf =  du.buildconfig([TESTSOURCE])
    assert(
        conf == {'SOURCEPATH': TESTSOURCE,
                 'SERVER': 'http://localhost:5000',
                 'APIKEYVAR': 'TEST_CKAN_APIKEY',
                 'PKGNAME': 'test_pkgname'})

    # SERVER: configfile, APIKEY: CLI
    conf =  du.buildconfig(['-a', 'apikey', TESTSOURCE])
    assert(
        conf == {'SOURCEPATH': TESTSOURCE,
                 'SERVER': 'http://localhost:5000',
                 'APIKEYVAR': 'apikey',
                 'PKGNAME': 'test_pkgname'})
    
    # PKGNAME missing
    with pt.raises(SystemExit):
        conf =  du.buildconfig(['-a', 'apikey', TESTSOURCE_EMPTY])


def test_readsource():
    with pt.raises(ValueError):
        du.readsource('this/path/not/exist')
    res = du.readsource(TESTSOURCE_LARGE)
    assert(res == {
        '500m': 524288000,
        'oneg': 1073741824,
        'onek': 1024,
        'onem': 1048576
        })
    with pt.raises(SystemExit):
        res = du.readsource(TESTSOURCE_EMPTY)
    

# This test depends on availibility of specific CKAN server        
def test_getpackage():
    pkg_exist = 'empty-test-for-bulk-upload'
    pkg_nonexist = 'non-existin g and-illegal&package'
    config = du.buildconfig(['-p', pkg_exist,
                             '-a', 'CKAN_APIKEY_PROD1',
                             '-s', 'https://data.eawag.ch',
                             TESTSOURCE])
    conn = du._get_conn(config)
    res = du.getpackage(conn, config)
    assert(res['name'] == pkg_exist)

    config['PKGNAME'] = pkg_nonexist
    with pt.raises(ValueError):
        res = du.getpackage(conn, config)
