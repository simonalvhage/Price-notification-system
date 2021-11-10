from bs4 import BeautifulSoup
import requests,re

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
HEADERS2 = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15', 'Accept-Language': 'sv-se', 'Accept': 'test/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

def parsewebsite_amazon(url):
    page = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(page.content, "lxml")
    title = soup.find("span", attrs={'id': 'productTitle'}).string.strip()
    img = soup.find("img", attrs={'id': 'landingImage'})
    img = img['data-a-dynamic-image']
    img = re.findall('"([^"]*)"', img)[0]
    price = soup.find("span", attrs={'id': 'priceblock_ourprice'}).string.strip().replace(u'\xa0', u' ')
    return title,img,price

def parsewebsite_netonnet(url):
    page = requests.get(url, headers=HEADERS2)
    soup = BeautifulSoup(page.content, "lxml")
    title = str(soup.find("div", attrs={'class': 'subTitle big'}))
    title = re.search('<h1>(.*)</h1>', title).group(1)
    imgurl = soup.find("img", attrs={'class': 'productImage'})
    imgurl = "https://www.netonnet.se/" + str(imgurl['data-src'])
    price = soup.find_all("div", attrs={'class': 'price-big'})[0].string.strip().replace(u':-', u' kr').replace(u'\xa0', u' ')
    if 'mån' in price:
        price = soup.find_all("div", attrs={'class': 'price-big'})[1].string.strip().replace(u':-', u' kr').replace(
            u'\xa0', u' ')
    return title,imgurl,price

def parsewebsite_elgiganten(url):
    page = requests.get(url, headers=HEADERS2)
    soup = BeautifulSoup(page.content, "lxml")
    title = str(soup.find("h1", attrs={'class': 'product-title'})).strip()
    title = re.search('">(.*)</h1>', title).group(1)
    imgurl = soup.find("img", attrs={'class': 'first-product-image'})
    imgurl = "https://www.elgiganten.se/" + str(imgurl['src'])
    price = str(soup.find("div", attrs={'class': 'product-price-container'}))
    if "None" in price:
        price = soup.find("span", attrs={'class': 'text-right price-pay table-cell'})
        price = price.find('span').string.strip().replace(u'\xa0', u' ') + " kr"
    else:
        price = re.search('<span>(.*)</span>', price).group(1) + " kr"
        price = price.replace(u'\xa0', u' ')
    return title,imgurl,price
