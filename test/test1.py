#coding:utf8
import urllib

url = 'http://m10.music.126.net/20180521224809/a89ed7140a98de5dd46e5bfed6716003/ymusic/fa3c/6658/3cf6/18858abde8922694c6ac3d37805b779d.mp3'
url = url.encode('gbk', 'replace')
urllib.quote_plus(url.encode('utf-8', 'replace'))


url = 'http://test.com/s?wd=哈哈'
url = url.decode('gbk', 'replace')
print urllib.quote(url.encode('utf-8', 'replace'))