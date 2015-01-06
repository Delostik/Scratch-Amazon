__author__ = 'Delostik'

import urllib2
from BeautifulSoup import BeautifulSoup
from string import atoi
import re

base_url = "http://www.amazon.com"


def get_html(url):
    request = urllib2.Request(url)
    request.add_header('User-Agent', "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36")
    response = urllib2.urlopen(request)
    try:
        html = response.read()
    except:
        print "Failed while connecting destination url..."
        exit(0)
    # delete comments
    html = re.compile('<!--[^>]*-->').sub('', html)
    return html


def process_comments(url):
    name = url.split("/")[3]

    html = get_html(url)
    # get number of pages
    soup = BeautifulSoup(html, fromEncoding="utf-8")
    spans = soup.find('span', 'paging')
    pages = spans.findAll('a')[1].text
    file = open("./res/" + name, 'w+')
    # process each page
    for i in range(1, atoi(pages) + 1):
        spilt_url = url.split('pageNumber')
        url_child = spilt_url[0] + "pageNumber=" + str(i) + "&showViewpoints=0&sortBy=byRankDescending"
        print "processing: " + name + "  page: " + str(i)
        response = urllib2.urlopen(url_child)
        try:
            html = response.read()
        except:
            print "Internet disconnect while scratching..."
            exit(0)
        reviews = soup.findAll('div', 'reviewText')
        for item in reviews:
            item = str(item).replace('<br />', '.').replace('<div class="reviewText">', '').replace('</div>', '')
            file.write('**********EXAMPLE START**********\n')
            file.write(str(item) + '\n')
            file.write('**********EXAMPLE END**********\n\n')
    file.close()


def get_next_page(html):
    soup = BeautifulSoup(html, fromEncoding="utf-8")
    next_page = soup.findAll('a', 'pagnNext')
    if (next_page):
        next_page = base_url + next_page[0].get('href')
        return next_page
    else:
        return 0


def scratch(url):
    while 1:
        html = get_html(url)
        soup = BeautifulSoup(html, fromEncoding="utf-8")
        divs = soup.findAll("div", "a-row a-spacing-top-mini a-spacing-none")
        for item in divs:
            item = item.find("a", "a-size-small a-link-normal a-text-normal").get('href')
            comment_url = item.split("ref=")[0] + "ref=cm_cr_pr_top_link_1?ie=UTF8&pageNumber=1&showViewpoints=0&sortBy=byRankDescending"
            process_comments(comment_url)
        next_page = soup.findAll('a', 'pagnNext')
        if (next_page):
            url = base_url + next_page[0].get('href')
        else:
            print "Done!"
            exit(0)


url = input()
scratch(url)

