import urllib.request
url = "https://firebasestorage.googleapis.com/v0/b/mtl-sentence-representations.appspot.com/o/data%2FMNLI.zip?alt=media&token=50329ea1-e339-40e2-809c-10c40afff3ce"
content = urllib.request.urlopen(url).read()
zipfile = open("data.zip", "wb")
zipfile.write(content)
zipfile.close()
