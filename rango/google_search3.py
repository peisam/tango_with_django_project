import sys
import urllib2,urllib
import json

reload(sys)
sys.setdefaultencoding('utf-8')

class getGooglepage:
    def __init__(self,):
        self.cx = '012080660999116631289:zlpj9ypbnii'
        self.key = 'AIzaSyCA6kcexRtocKVOzCjmjSYf0ifxYh1epew'
    def getpage(self, query):
        results = []
        url = ('https://www.googleapis.com/customsearch/v1?'
                '&key=%s'
                '&cx=%s'
                '&q=%s'
                ) % (self.key, self.cx, urllib.quote(query))
        request = urllib2.Request(url, None)
        response = urllib2.urlopen(request).read()
        #h = HTMLParser.HTMLParser()
        #print (h.unescape(response))
        json_response = json.loads(response)
        for result in json_response['items']:
            results.append({
                'title': result['title'],
                'link': result['formattedUrl'],
                'summary': result['snippet']})
    # Return the list of results to the calling function.
        return results
    def __call__(self, query):
        return self.getpage(query)


if __name__ == '__main__':
    test = getGooglepage()
    keyword = 'python'
    test.getpage(keyword)