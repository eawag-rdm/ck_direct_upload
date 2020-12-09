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
    res = du._getargs(['/the/path/to/hell','-a', 'keyenv', '-s', 'somehost'])
    assert(res['--help'] is False
           and res['-s'] == 'somehost'
           and res['-a'] == 'keyenv'
           and res['SOURCEPATH'] == '/the/path/to/hell')
    res = du._getargs(['/the/path/to/hell'])
    assert(res['--help'] is False
           and res['-s'] is None and res['-a'] is None)
 
    
    
def test_readsource():
    with pt.raises(ValueError):
        du.readsource('this/path/not/exist')
    
def test__readconfig():
    res = du._readconfig(TESTSOURCE)
    assert(res == {'APIKEYVAR': 'TEST_CKAN_APIKEY',
                   'SERVER': 'http://localhost:5000'})


def test_buildconfig():
    # just configfile
    conf = du.buildconfig([TESTSOURCE])
    assert(
        conf == {'SOURCEPATH': TESTSOURCE,
                  'SERVER': 'http://localhost:5000',
                  'APIKEYVAR': 'TEST_CKAN_APIKEY'})

    # Both default
    conf =  du.buildconfig([TESTSOURCE_EMPTY])
    assert(
        conf == {'SOURCEPATH': TESTSOURCE_EMPTY,
                  'SERVER': 'https://data.eawag.ch',
                  'APIKEYVAR': 'CKAN_APIKEY_PROD1'})

    # SERVER: CLI, APIKEY: default    
    conf =  du.buildconfig(['-s', 'testserver', TESTSOURCE_EMPTY])
    assert(
        conf == {'SOURCEPATH': TESTSOURCE_EMPTY,
                 'SERVER': 'testserver',
                 'APIKEYVAR': 'CKAN_APIKEY_PROD1'})

    # SERVER: default,  APIKEY: configfile
    conf =  du.buildconfig([TESTSOURCE])
    assert(
        conf == {'SOURCEPATH': TESTSOURCE,
                 'SERVER': 'http://localhost:5000',
                 'APIKEYVAR': 'TEST_CKAN_APIKEY'})

    # SERVER: configfile, APIKEY: CLI
    conf =  du.buildconfig(['-a', 'apikey', TESTSOURCE])
    assert(
        conf == {'SOURCEPATH': TESTSOURCE,
                 'SERVER': 'http://localhost:5000',
                 'APIKEYVAR': 'apikey'})

