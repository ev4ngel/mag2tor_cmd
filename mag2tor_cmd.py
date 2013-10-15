#-*- encoding:utf8 -*-
import sys, re, os
USE_HOW="""
mag2tor ["magnet_link"] [path_to_download]
                     magnet_link must be Quoted by Double Qoutes

mag2tor [@magnet_file] [Path_to_download]     
                     magnet_file must be a file with magnet(s) per line
"""
from dooo import *
defaultpath=os.path.join(os.getcwd(),"torrents")
def usage():
    print USE_HOW
def noQuotesWarning(_mag):
    if len(_mag)==40:# I dont know how to exclude the unquoted magnet or just a file
        usage()
        sys.exit(1)
def getPath():
    _path=raw_input("\nPath[Default:{0}]:\n".format(defaultpath))
    if _path=="":
        _path=defaultpath
    if not os.path.exists(_path):
        try:
            os.mkdir(_path)
        except WindowError:
            print "Something Happened When Building Directory [{0}]".format(_path)
            sys.exit(1)
    return _path
def mgts2list(mag):
    mgts=[]
    if type(mag)==type(""): 
        if mag.startswith("@"):
            f=open(mag[1:], 'r')
            for fm in f:
                mgts.append(Magnet(fm))
            f.close()
        else:
            mgts.append(Magnet(mag))
    return mgts
def noParam( ):
    _mag=raw_input("Magnet:\n")
    if _mag=="":
        usage()
        sys.exit(1)
    _path=getPath()
    twoParams(_mag, _path)
def oneParam(_mag):
    noQuotesWarning(_mag)
    _path=getPath()
    twoParams(_mag, _path)
def twoParams(_mag, _path):
    noQuotesWarning(_mag)
    mgts=mgts2list(_mag)
    tsmgr=TorrentStoreManager()
    tsmgr.initFromXML()
    for _mag in mgts:
        for ts in tsmgr.torrentStores():
            print "[{0}]Trying ...".format(ts.getUrl())
            tg=TorrentGetter(ts, _mag, _path)
            rlt=tg.download()
            if rlt:
                print "[OK]"+_mag.title().decode("utf8")
                break
if __name__=="__main__":
    argc=len(sys.argv)-1
    deal=[ noParam, oneParam, twoParams]
    deal[argc](*sys.argv[1:])

