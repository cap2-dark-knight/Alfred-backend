from .models import CrawledData, Keyword, Profile, SmartKeywordInfo
from .crawler import general_crawler, smart_crawler

def crawl():
    keywords = Keyword.objects.all()
    for keyword in keywords:
        datalist = []
        if keyword.get_smartkeywordinfo() == None : 
            datalist = general_crawler(keyword.keyword)
        else:
            selector = keyword.get_smartkeywordinfo()
            type = selector['type']
            datalist = smart_crawler(type, keyword.keyword, selector)
        for d in datalist :
            CrawledData.objects.create(keywords=keyword, url=d['url'], title=d['title'], content=d['contents'], image_url=d['img'])


