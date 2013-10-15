#-*- encoding:utf8 -*-
import urllib, urllib2,re,sys, os
from xml.etree.ElementTree import *
class Magnet():
    def __init__(self,mgt=None):
        if mgt!=None:
            self.parseMagnet(mgt)
    def hashcode(self):
        return self.__hashcode
    def title(self):
        return self.__title
    def tracks(self):
        return self.__tracks
    def setTitle(self,title):
        self.__title=title
    def setHashcode(self,hashcode):
        self.__hashcode=hashcode
    def setTracks(self, tracks):
        self.__tracks=tracks
    def parseMagnet(self,mgt):
        partial=re.search(r'btih:(.*)&dn=(.*?)(&tr=.*)',mgt)
        try:
            self.__hashcode=partial.group(1)
            self.__title=urllib.unquote(partial.group(2))
            self.__tracks=[]
            ts=partial.group(3).split("&tr=")
            for tts in ts:
                if len(tts)==0:
                    continue
                self.__tracks.append(urllib.unquote(tts))
        except AttributeError:
            print "The Magnet Failed!"
    def __str__(self):
        return "magnet:?xt=urn:btin:{0}&dn={1}&tr={2}".format(self.__hashcode,urllib.quote(self.__title),"&tr=".join(self.__tracks))

"""
{url}/(hashcode:0:2}/{hashcode:-2:0}/{hashcode}.torrent
{url}/{hashcode}.torrent

{title}=magnet.title
{hashcode}=magnet.hashcode

"""
class TorrentGetter():
    def __init__(self,torrentstore,magnet,targetpath=os.getcwd()):
        self.url=torrentstore.parseMagnet(magnet)
        self.title=magnet.title()
        self.target=targetpath
    def download(self):
        try: 
            opn=urllib2.urlopen(self.url)
            trt=opn.read()
            with open(os.path.join(self.target,self.title.decode("utf8")+".torrent"), 'wb') as f:
                f.write(trt)
            return True
        except urllib2.HTTPError as he:
            print he.message
            return False
            
class TorrentStoreManager():
    def __init__(self):
        self.__torrentStores=[]
        self.__orderedTorrents=[]
        self.__highestPri=1
        self.__lowestPri=999
    def add(self,tt):        
        self.__torrentStores.append(tt)
        self.__lowestPri+=1
        tt.setPrivilege(self.__lowestPri)
        self._updatePri()
    def initFromXML(self,xmlpath='template.xml'):
        root=ElementTree()
        allTs=root.parse(xmlpath).findall("torrent")
        tmptt=[]
        for e in allTs:
            tt=TorrentStore()
            tt.initFromElement(e)
            tmptt.append(tt)
        self.__torrentStores=[tx for tx in sorted(tmptt,lambda x,y:cmp(x.getPrivilege(),y.getPrivilege()))]
        self.__lowestPri=self.__torrentStores[-1].getPrivilege()
        self.__highestPri=self.__torrentStores[0].getPrivilege()
    def writeXML(self,xmlpath="template.xml"):
        tree=ElementTree()
        root=Element("ts")
        for t in self.__torrentStores:
            root.append(t.toElement())
        tree._setroot(root)
        tree.write(xmlpath)
    def _updatePri(self,):
        pri=self.__highestPri
        for t in self.__torrentStores:
            t.setPrivilege(pri)
            pri+=1
        self.__lowestPri=pri
    def deleteAt(self,index):
        del self.__torrentStores[index]
    def upAt(self,index):
        if index!=0:
            self.__torrentStores[index],self.__torrentStores[index-1]=self.__torrentStores[index-1],self.__torrentStores[index]
            self._updatePri()
    def downAt(self,index):
        if index<len(self.__torrentStores)-1:
            self.__torrentStores[index],self.__torrentStores[index+1]=self.__torrentStores[index+1],self.__torrentStores[index]
            self._updatePri()
    def torrentStores(self):
        return self.__torrentStores
            
class TorrentStore:
    def __init__(self,url=None,template=None,tag=None,privilege=None,manager=None):
        self.__tag=tag
        self.__url=url
        self.__template=template
        self.__privilege=privilege
        self.__manager=manager
    def getUrl(self):
        return self.__url
    def getTag(self):
        return self.__tag
    def hasManager(self):
        return self.__manager is not None
    def setManager(self,manager):
        self.__manager=manager
    def getPrivilege(self):
        return self.__privilege
    def setPrivilege(self,pri):
        self.__privilege=pri
    def initFromElement(self,element):
        self.__tag=element.find("tag").text
        self.__url=element.find("url").text
        self.__privilege=int(element.find("privilege").text)
        self.__template=element.find("template").text
    def toElement(self):
        e=Element("torrent")
        tag=Element("tag")
        tag.text=self.__tag
        url=Element("url")
        url.text=self.__url
        template=Element("template")
        template.text=self.__template
        pri=Element("privilege")
        pri.text=str(self.__privilege)
        e.append(tag)
        e.append(url)
        e.append(template)
        e.append(pri)
        return e
    def parseMagnet(self, _magnet):
        rdict={'hashcode':_magnet.hashcode(), 'url':self.__url, 'title':_magnet.title()}
        _dlurl=self.__template
        rs=re.findall(r'\{[:\w-]+?\}', _dlurl)
        for rss in rs:
            key=rss[1:-1]
            if key in rdict:
                _dlurl=_dlurl.replace(rss, rdict[key])
            else:
                rks=key.split(":")
                rks.extend([None]*2)
                rks=rks[:3]
                s=None if rks[1]=="" else int(rks[1])
                e=None if rks[2]=="" else int(rks[2])                
                _dlurl=_dlurl.replace(rss, rdict[rks[0]][slice(s, e)])
        return _dlurl
if __name__=="__main__":        
    pass
