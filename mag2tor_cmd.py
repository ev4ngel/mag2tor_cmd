#-*- encoding:utf8 -*-
import sys, re, os
"""
mag2tor ["magnet_link"] [path_to_download]
"""
from dooo import *
defaultpath=os.getcwd()
def noParam( ):
    _mag=raw_input("Magnet:")
    _path=raw_input("Path[Default:{0}]:".format(defaultpath))
    if _path=="":
        _path=defaultpath
    twoParams(_mag, _path)
def oneParam(_mag):
    if len(_mag)==60:
        print "\n\n\nPlease Enbrace The magnet with \"\""
        print "Please Enbrace The magnet with \"\""
        print "Please Enbrace The magnet with \"\"\n\n\n\n"
        sys.exit(1)
    _path=raw_input("Path[Default:{0}]:".format(defaultpath))
    if _path=="":
        _path=defaultpath
    twoParams(_mag, _path)
def twoParams(_mag, _path):
    if len(_mag)==60:
        print "\n\n\nPlease Enbrace The magnet with \"\""
        print "Please Enbrace The magnet with \"\""
        print "Please Enbrace The magnet with \"\"\n\n\n\n"
        sys.exit(1)
    magnet=Magnet(_mag)
    tsmgr=TorrentStoreManager()
    tsmgr.initFromXML()
    for ts in tsmgr.torrentStores():
        print "[{0}]Trying ...".format(ts.getUrl())
        tg=TorrentGetter(ts, magnet, _path)
        rlt=tg.download()
        if rlt:
            print "[OK]"+magnet.title().decode("utf8")
            break
if __name__=="__main__":
    argc=len(sys.argv)-1
    deal=[ noParam, oneParam, twoParams]
    deal[argc](*sys.argv[1:])

