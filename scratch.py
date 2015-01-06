__author__ = 'Delostik'


import urllib2
from BeautifulSoup import BeautifulSoup
from string import atoi
import re

base_url = 'www.amazon.com'

def process_good(url):
    request = urllib2.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36')
    response = urllib2.urlopen(request)
    try:
        html = response.read()
    except:
        print "Failed while connecting destination url..."
        exit(0)

    file = open('data', 'w+')

    # get number of pages
    soup = BeautifulSoup(html, fromEncoding="utf-8")
    soup = soup.find('span', 'paging')
    pages = soup.findAll('a')[1].text

    # process each page
    for i in range(1, atoi(pages) + 1):
        spilt_url = url.split('pageNumber')
        url_child = spilt_url[0] + "pageNumber=" + str(i) + "&showViewpoints=0&sortBy=byRankDescending"
        print "processing: " + url_child
        response = urllib2.urlopen(url_child)
        try:
            html = response.read()
        except:
            print "Internet disconnect while scratching..."
            exit(0)

        soup = BeautifulSoup(html)
        reviews = soup.findAll('div', 'reviewText')
        for item in reviews:
            item = str(item).replace('<br />', '.').replace('<div class="reviewText">', '').replace('</div>', '')
            file.write('**********EXAMPLE START**********\n')
            file.write(str(item) + '\n')
            file.write('**********EXAMPLE END**********\n\n')
    file.close()

"""
def get_goods_list(url):
    print url
    #exit(0)
    request = urllib2.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36')
    response = urllib2.urlopen(request)

    try:
        html = response.read()
    except:
        print "Failed while connecting destination url..."
        exit(0)

    # delete comments
    #html = re.compile('<!--[^>]*-->').sub('', html)
    print html
    soup = BeautifulSoup(html)
    print soup.a
    next_page = soup.findAll('a', 'pagnNext')
    print next_page[0].text
    if (next_page):
        #next_page = base_url + next_page[0].attr('href')
        next_page = next_page[0].get('href')
        print next_page
    else:
        print "no next page"

get_goods_list("http://www.amazon.com/s/ref=sr_pg_1?rh=n%3A2335752011%2Cn%3A7072561011%2Ck%3Axiaomi&keywords=xiaomi&ie=UTF8&qid=1420468626&lo=mobile")
"""

#process_good('http://www.amazon.com/Nokia-Lumia-520-GoPhone-AT/product-reviews/B00E45043A/ref=cm_cr_pr_top_link_2?ie=UTF8&pageNumber=1&showViewpoints=0&sortBy=byRankDescending')
while 1:
    url = input()
    process_good(url)