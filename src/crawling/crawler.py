import requests
from bs4 import BeautifulSoup

def naver_news(keyword): #general keyword
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

def saramin():
    saramin_url = "https://www.saramin.co.kr/zf_user/"
    raw = requests.get(saramin_url, headers={'User-Agent': 'Mozilla/5.0'})
    html = BeautifulSoup(raw.text, "html.parser")
    articles = html.select("ul.list_product > li.open")

    l = []

    for i in range(5):
        target_url = articles[i].select_one("a")['href']
        if "saramin.co.kr" not in target_url:
            target_url = "saramin.co.kr"+target_url
        title = articles[i].select_one('em.product_desc').text
        image = articles[i].select_one("img")['src']
        if "https:" not in image:
            image = "https:"+image
        dday = articles[i].select_one("span.num_dday")
        if dday is not None:
            contents = "("+dday.text+")"
        company = articles[i].select_one("strong.poduct_tit")
        if company is not None:
            contents = contents + " " + company.text

        job_dict = {'url':target_url, 'title':title, 'img':image, 'contents':contents}
        l.append(job_dict)

    return l

def wfootball():
    wfootball_url = "https://sports.news.naver.com/wfootball/index.nhn"
    raw = requests.get(wfootball_url, headers={'User-Agent': 'Mozilla/5.0'})
    html = BeautifulSoup(raw.text, "html.parser")
    articles = html.select('ol.news_list > li')

    l = []

    for i in range(5):
        target_url = "https://sports.news.naver.com" + articles[i].select_one('a')['href']
        title = articles[i].select_one("a.link_news_end").text
        image, contents = get_img_and_contents(target_url)
        wfootball_dict = {'url':target_url, 'title':title, 'img':image, 'contents':contents}
        l.append(wfootball_dict)

    return l

def kfootball():
    kfootball_url = "https://sports.news.naver.com/kfootball/index.nhn"
    raw = requests.get(kfootball_url, headers={'User-Agent': 'Mozilla/5.0'})
    html = BeautifulSoup(raw.text, "html.parser")
    articles = html.select('ol.news_list > li')

    l = []

    for i in range(5):
        target_url = "https://sports.news.naver.com" + articles[i].select_one('a')['href']
        title = articles[i].select_one("a.link_news_end").text
        image, contents = get_img_and_contents(target_url)
        kfootball_dict = {'url': target_url, 'title': title, 'img':image, 'contents':contents}
        l.append(kfootball_dict)

    return l

def basketball():
    basketball_url = "https://sports.news.naver.com/basketball/index.nhn"
    raw = requests.get(basketball_url, headers={'User-Agent': 'Mozilla/5.0'})
    html = BeautifulSoup(raw.text, "html.parser")
    articles = html.select('ol.news_list > li')

    l = []

    for i in range(5):
        target_url = "https://sports.news.naver.com" + articles[i].select_one('a')['href']
        title = articles[i].select_one("a.link_news_end").text
        image, contents = get_img_and_contents(target_url)
        basketball_dict = {'url': target_url, 'title': title, 'img':image, 'contents':contents}
        l.append(basketball_dict)

    return l

def wbaseball():
    wbaseball_url = "https://sports.news.naver.com/wbaseball/index.nhn"
    raw = requests.get(wbaseball_url, headers={'User-Agent': 'Mozilla/5.0'})
    html = BeautifulSoup(raw.text, "html.parser")
    articles = html.select('ol.news_list > li')

    l = []

    for i in range(5):
        target_url = "https://sports.news.naver.com" + articles[i].select_one('a')['href']
        title = articles[i].select_one("a.link_news_end").text
        image, contents = get_img_and_contents(target_url)
        wbaseball_dict = {'url':target_url, 'title':title, 'img':image, 'contents':contents}
        l.append(wbaseball_dict)

    return l

def kbaseball():
    kbaseball_url = "https://sports.news.naver.com/kbaseball/index.nhn"
    raw = requests.get(kbaseball_url, headers={'User-Agent': 'Mozilla/5.0'})
    html = BeautifulSoup(raw.text, "html.parser")
    articles = html.select('ol.news_list > li')

    l = []

    for i in range(5):
        target_url = "https://sports.news.naver.com" + articles[i].select_one('a')['href']
        title = articles[i].select_one("a.link_news_end").text
        image, contents = get_img_and_contents(target_url)
        kbaseball_dict = {'url':target_url, 'title':title, 'img':image, 'contents':contents}
        l.append(kbaseball_dict)

    return l

def golf():
    golf_url = "https://sports.news.naver.com/golf/index.nhn"
    raw = requests.get(golf_url, headers={'User-Agent': 'Mozilla/5.0'})
    html = BeautifulSoup(raw.text, "html.parser")
    articles = html.select('ol.news_list > li')

    l = []

    for i in range(5):
        target_url = "https://sports.news.naver.com" + articles[i].select_one('a')['href']
        title = articles[i].select_one("a.link_news_end").text
        image, contents = get_img_and_contents(target_url)
        golf_dict = {'url': target_url, 'title': title, 'img':image, 'contents':contents}
        l.append(golf_dict)

    return l

def politics():
    politics_url = "https://news.daum.net/politics#1"
    raw = requests.get(politics_url, headers={'User-Agent': 'Mozilla/5.0'})
    html = BeautifulSoup(raw.text, "html.parser")
    articles = html.select('ul.list_mainnews > li')

    l = []

    for i in range(len(articles)):
        target_url = articles[i].select_one('a')['href']
        title = articles[i].select_one('img')['alt']
        image = articles[i].select_one('img')
        if image is not None:
            image = image['src']
        contents = get_contents(target_url)
        if len(contents) >= 60:
            contents = contents[:57] + "..."

        politics_dict = {'url':target_url, 'title':title, 'img':image, 'contents':contents}
        l.append(politics_dict)

    return l

def economy():
    economy_url = "https://news.daum.net/economic/#1"
    raw = requests.get(economy_url, headers={'User-Agent': 'Mozilla/5.0'})
    html = BeautifulSoup(raw.text, "html.parser")
    articles = html.select('ul.list_mainnews > li')

    l = []

    for i in range(len(articles)):
        target_url = articles[i].select_one('a')['href']
        title = articles[i].select_one('img')['alt']
        image = articles[i].select_one('img')
        if image is not None:
            image = image['src']
        contents = get_contents(target_url)
        if len(contents) >= 60:
            contents = contents[:57] + "..."

        economy_dict = {'url':target_url, 'title':title, 'img':image, 'contents':contents}
        l.append(economy_dict)

    return l

def IT():
    IT_url = "https://news.daum.net/digital#1"
    raw = requests.get(IT_url, headers={'User-Agent': 'Mozilla/5.0'})
    html = BeautifulSoup(raw.text, "html.parser")
    articles = html.select('ul.list_mainnews > li')

    l = []

    for i in range(len(articles)):
        target_url = articles[i].select_one('a')['href']
        title = articles[i].select_one('img')['alt']
        image = articles[i].select_one('img')
        if image is not None:
            image = image['src']
        contents = get_contents(target_url)
        if len(contents) >= 60:
            contents = contents[:57] + "..."

        IT_dict = {'url': target_url, 'title': title, 'img': image, 'contents': contents}
        l.append(IT_dict)

    return l

def get_contents(url): #daum news
    raw = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = BeautifulSoup(raw.text, "html.parser")
    contents = html.select_one('div.news_view').get_text('\n', strip=True)

    return contents

def get_img_and_contents(url): #naver sports
    raw = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = BeautifulSoup(raw.text, "html.parser")
    img = html.select_one('span.end_photo_org > img')
    if img is not None:
        img = img['src']
    contents = html.select_one('div#newsEndContents').get_text('\n', strip=True)
    contents_list = contents.split('\n')
    txt = contents_list[2]
    if len(txt) >= 60:
        txt = txt[:57] + "..."

    return img, txt

def main():
    keyword = input("keyword : ")

    if keyword in ['코로나']:
        l = naver_news(keyword)

    elif keyword in ['취업', '공채']:
        l = saramin()

    elif keyword in ['해외축구', '해축']:
        l = wfootball()

    elif keyword in ['국내축구', 'k리그', 'K리그', '한국축구']:
        l = kfootball()

    elif keyword in ['농구', 'basketball']:
        l = basketball()

    elif keyword in ['해외야구', 'MLB']:
        l = wbaseball()

    elif keyword in ['국내야구', 'KBO']:
        l = kbaseball()

    elif keyword in ['골프', 'golf']:
        l = golf()

    elif keyword in ['정치', 'politics']:
        l = politics()

    elif keyword in ['경제', 'ecomony']:
        l = economy()

    elif keyword in ['IT', '기술', 'IT/기술']:
        l = IT()

    else:
        l = naver_news(keyword)

    # test print
    for i in range(len(l)):
        print('[{}]'.format(i+1))
        print(l[i]['url'])
        print(l[i]['title'])
        print(l[i]['img'])
        print(l[i]['contents'])

if __name__ == "__main__":
    main()

