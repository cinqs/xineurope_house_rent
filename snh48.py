import requests as re
from html.parser import HTMLParser as hp


class IndexHTMLParser(hp):
    foundDiv = False;
    foundTitle = False;
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if self.foundDiv and tag == 'img':
            imageUrl = 'http://www.snh48.com/' + attrs.get('src');
            imageName = attrs.get('alt');
            print(imageName)
            r = re.get(imageUrl, stream=True)
            if r.status_code == 200:
                with open('/tmp/snh48/' + imageName + '.jpg', 'wb') as f:
                    for chunk in r:
                        f.write(chunk)

        if attrs.get('class') == 'mem_p':
            self.foundDiv = True
        else:
            self.foundDiv = False

    def handle_data(self, data):
        if self.foundTitle:
            print(data)

indexParser = IndexHTMLParser()

for i in range(10001, 10171):
    print(i)
    res = re.get('http://www.snh48.com/member_detail.php?sid=' + str(i))
    res.encoding = 'utf-8'
    indexParser.feed(str(res.text))