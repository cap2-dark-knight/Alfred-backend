import requests
from bs4 import BeautifulSoup

def get_time(url):
    r = requests.get(url, headers={'User-Agent':'Mozilla/5.0'})
    soup = BeautifulSoup(r.text, "html.parser")
    #TODO

def politics():
    url = "https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=100"
    raw = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = BeautifulSoup(raw.text, "html.parser")
    articles = html.select("div.cluster > div.cluster_group")
    print(articles[0])
    print("-----------------")
    for i in range(1, 6):
        #target_url = articles[i].select_one("a.cluster_text_headline")
        print("a")
        #print(target_url)

def naver_news(keyword):
    news_url = "https://search.naver.com/search.naver?where=news&query="

    raw = requests.get(news_url+keyword, headers={'User-Agent':'Mozilla/5.0'})
    html = BeautifulSoup(raw.text, "html.parser")
    articles = html.select("ul.list_news > li")

    for i in range(5):
        target_url = articles[i].select_one("a")["href"]
        title = articles[i].select_one("a.news_tit").text
        image = articles[i].select_one("img.thumb.api_get")["src"]
        contents = articles[i].select_one("div.news_dsc").text
        contents = contents[:60]+"..."
        #time = articles[i].select_one("span.info").text
        #time = get_time(target_url)

        print("[{0}]".format(i+1))
        print(target_url)
        print(title)
        print(image)
        print(contents)
        #print(time)
        print("\n")

def Kbaseball():#국내 야구
    url = "https://sports.news.naver.com/kbaseball/news/index.nhn?isphoto=N"

    raw = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = BeautifulSoup(raw.text, "html.parser")
    articles = html.select("div#_newsList.news_list")
    print(articles)
    for i in range(5):
        #target_url = articles[i].select_one("a")["href"]
        title = articles[i].select_one("a.title").text
        #image = articles[i].select_one("span.mask")
        #contents = articles[i].select_one("p.desc")
        #contents = contents[:60] + "..."

        print("[{0}]".format(i + 1))
        #print(target_url)
        print(title)
        #print(image)
        #print(contents)
        print("\n")

def main():
    keyword = input("keyword : ")

    if keyword in ['정치', '경제']:
        naver_news(keyword)
    elif keyword in ['국내야구']:
        Kbaseball();
    else:
        print("normal crawler")

if __name__ == "__main__":
    main()

