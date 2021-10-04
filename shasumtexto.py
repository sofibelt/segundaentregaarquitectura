import sys
import hashlib

def shasumtexto(data):
    # BUF_SIZE is totally arbitrary, change for your app!
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

    md5 = hashlib.md5()
    sha1 = hashlib.sha1()

    md5.update(data)
    sha1.update(data)

    #print("MD5: {0}".format(md5.hexdigest()))
    #print("SHA1: {0}".format(sha1.hexdigest()))
    return sha1.hexdigest()
