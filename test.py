import requests as re
from html.parser import HTMLParser as hp
import pymysql as pm

conn = pm.connect(host = 'localhost', user = 'guest', password = 'test@guest', db = 'test', charset='utf8mb4')
cur = conn.cursor()
index = list()


class IndexHTMLParser(hp):
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('onclick') == 'atarget(this)':
            href = str(attrs.get('href'))
            if len(href) > 0:
                index.append(href)

    def handle_endtag(self, tag):
        self.end_tag = tag

indexParser = IndexHTMLParser()

for i in range(1):
    res = re.get('http://buy.xineurope.com/forum.php?mod=forumdisplay&fid=10&page=' + str(i))
    indexParser.feed(str(res.text))

for i in range(0, len(index)):
    sql = 'insert into urls values(\'' + index[i] + '\')'
    cur.execute(sql)

#conn.commit()

class PageHTMLParser(hp):
    number = 0
    content = dict()
    tag_found = False
    value_found = False
    current_tag = ''
    mobile_found = False

    def handle_starttag(self, tag, attrs):
        if tag == 'dd' and self.tag_found:
            self.value_found = True
        else:
            self.value_found = False

        if tag == 'dt':
            self.tag_found = True
        else:
            self.tag_found = False

        if '手机' in self.current_tag and tag == 'strong':
            self.mobile_found = True
        else:
            self.mobile_found = False
    def handle_endtag(self, tag):
        self.end_tag = tag

    def handle_data(self, data):
        data = data.strip()
        if self.tag_found:
            if len(data) > 0:
                self.current_tag = data
        if self.value_found or self.mobile_found:
            if len(data) > 0:
                self.content[self.current_tag] = data

def get_value(res, attr):
    if attr in res:
        return '\"' + res[attr] + '\"'
    else:
        return '\"\"'

for i in range(0, len(index)):
    url = index[i]
    print(url)
    res = re.get(url)
    pageParser = PageHTMLParser()
    pageParser.feed(str(res.text))
    result = dict(pageParser.content)
    print(result)
    sql = 'insert into houses values(' + get_value(result, '房屋面积:') + ',' + get_value(result, '房屋租金:') + ',' + get_value(result, '房屋押金:') \
          + ',' + get_value(result, '房屋类型:') + ',' + get_value(result, '公交线路:') + ',' + get_value(result, '联系人:') \
          + ',' + get_value(result, '手机:') + ',' + get_value(result, '地址:') + ')'
    print(sql)
    cur.execute(sql)



conn.commit()


conn.close()