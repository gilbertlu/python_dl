import sys
import urllib, urllib2, cookielib

from HTMLParser import HTMLParser

# 300 to 399 has been downloaded
# 302, 364 empty, 365 to 370 not yet download
BOOK_NO_START = 364
BOOK_NO_END   = 365

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag != 'a': return
        for name, value in attrs:
            if name == 'href':
                if value[1:7] == 'go.php':
                    self.gophp = value
                    return



def parse_url_dl(url, book_num):
    url_book = url + '/book/' + str(book_num)
    print url_book

    req = urllib2.Request(url_book)
    #print "req = ", req
    u = urllib2.urlopen(req)
    webContent = u.read().decode('utf_8')
    #print "webContent = ", webContent
    parser = MyHTMLParser()
    parser.feed(webContent)
    #if not isexist(parser.gophp):
    #    print "it is empty"
    print "gophp = ", parser.gophp
    url_dl = url + parser.gophp
    print "book down load = ", url_dl
    u.close()
    return url_dl



def parse_url_file(u_dl):
    meta = u_dl.info()
    file_len = meta.get("Content-Length")
    print "Total File Length = ", file_len
    Content_Disposition = meta.get("Content-Disposition")
    file_name = Content_Disposition.split("filename=")
    print "Down load: ", file_name[1]
    return file_len, file_name[1]



def dl_file(file_len, file_name, u_dl):
    fp = open(file_name, 'wb')
    file_size_dl = 0
    block_sz = 8192
    percentage = 0
    while True:
        buffer = u_dl.read(block_sz)
        file_size_dl += len(buffer)
        ptg = int(file_size_dl*100/float(file_len))
        
        if (ptg > percentage):
            percentage = ptg
            print percentage,"%\r",
                       
        if not buffer:
            break
        fp.write(buffer)
            
    fp.close()
    print "..."
    print "file close"



def main():
    book_range = range(BOOK_NO_START, BOOK_NO_END)
    for book_num in book_range:
        url      = 'http://it-ebooks.info'
        url_dl = parse_url_dl(url, book_num)

        req_dl = urllib2.Request(url_dl)
        u_dl = urllib2.urlopen(req_dl)
        file_len, file_name = parse_url_file(u_dl)  
        dl_file(file_len, file_name, u_dl)
        u_dl.close()
        print "u_dl close"



if __name__ == "__main__":
    main()
  
