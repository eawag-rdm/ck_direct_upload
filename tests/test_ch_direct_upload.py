import pytest as pt
import ck_direct_upload as du

def test_getargs():
    with pt.raises(SystemExit):
        res = du.getargs(["-h"])
    res = du.getargs(['/the/path/to/hell'])
    assert(res['--help'] is False
           and res['-s'] == 'https://data.eawag.ch'
           and res['-a'] == 'CKAN_APIKEY_PROD1'
           and res['PATH'] == '/the/path/to/hell')
    
def test_readsource():
    with pt.raises(ValueError):
        du.readsource('this/path/not/exist')
#    res = du.readsource('./test/data')

