import urllib
from smb.SMBHandler import SMBHandler
opener = urllib.request.build_opener(SMBHandler)
fh = opener.open('smb://host/share/file.txt')
data = fh.read()
fh.close()