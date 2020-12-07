import requests
from bs4 import BeautifulSoup

def general_crawler(keyword): 
    news_url = "https://search.naver.com/search.naver?where=news&query="

    raw = requests.get(news_url+keyword, headers={'User-Agent':'Mozilla/5.0'})
    html = BeautifulSoup(raw.text, "html.parser")
    articles = html.select("ul.list_news > li")

    l = []

    for i in range(5):
        target_url = articles[i].select_one("a")["href"]
        title = articles[i].select_one("a.news_tit").text
        image = articles[i].select_one("img.thumb.api_get")
        if image is not None:
            image = image["src"]
        contents = articles[i].select_one("div.news_dsc").text
        if len(contents) >= 60:
            contents = contents[:57]+"..."

        news_dict = {'url' : target_url, 'title' : title, 'img' : image, 'contents' : contents}
        l.append(news_dict)

    return l


def smart_crawler(type, keyword, selector):
    try:
        url = selector['url']
        raw = requests.get(url, headers={'User-Agent':'Mozilla/5.0'})
        html = BeautifulSoup(raw.text, "html.parser")
        articles = html.select(selector['articles'])
        l = []
        
        articles_len = len(articles)
        if articles_len > 5:
            articles_len = 5 
        
        for i in range(articles_len):
            if type=="naver" :
                l.append(smart_crawler_naver(selector, articles[i]))
            elif type == "saramin" :
                l.append(smart_crawler_saramin(selector, articles[i]))
            elif type == "daum":
                l.append(smart_crawler_daum(selector, articles[i]))

        if len(l) == 0 :
            return general_crawler(keyword)
        return l
    except:
        return general_crawler(keyword)



def smart_crawler_naver(selector, article):    
    target_url = selector['target_base']+article.select_one("a")["href"]
    title = article.select_one(selector['title']).text

    target_raw = requests.get(target_url, headers={'User-Agent': 'Mozilla/5.0'})
    target_html = BeautifulSoup(target_raw.text, "html.parser")
    img = target_html.select_one(selector['image'])
    if img is not None:
        img = img['src']
    contents = target_html.select_one(selector['contents']).get_text('\n', strip=True)
    contents_list = contents.split('\n')
    txt = contents_list[2]
    if len(txt) >= 60:
        txt = txt[:57] + "..."
    news_dict = {'url' : target_url, 'title' : title, 'img' : img, 'contents' : txt} 
    return news_dict

def smart_crawler_daum(selector, article):    
    target_url = article.select_one("a")["href"]
    title = article.select_one('img')['alt']
    img = article.select_one('img')
    if img is not None:
            img = img['src']

    raw = requests.get(target_url, headers={'User-Agent': 'Mozilla/5.0'})
    html = BeautifulSoup(raw.text, "html.parser")
    contents = html.select_one('div.news_view').get_text('\n', strip=True)
    if len(contents) >= 60:
            contents = contents[:57] + "..."
    news_dict = {'url' : target_url, 'title' : title, 'img' : img, 'contents' : contents} 
    return news_dict

def smart_crawler_saramin(selector, article):
    target_url = article.select_one("a")['href']
    if "saramin.co.kr" not in target_url:
        target_url = "saramin.co.kr"+target_url
    title = article.select_one('em.product_desc').text
    image = article.select_one("img")['src']
    if "https:" not in image:
        image = "https:"+image
    dday = article.select_one("span.num_dday")
    contents = ""
    if dday is not None:
        contents = "("+dday.text+")"
    company = article.select_one("strong.poduct_tit")
    if company is not None:
        contents = contents + " " + company.text

    job_dict = {'url':target_url, 'title':title, 'img':image, 'contents':contents}
    return job_dict
    
