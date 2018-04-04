# -*- coding: utf-8 -*-

import requests
from lxml import html


TYPE_SEARCH = {
    "all": "all",
    "movie": "tt",
    "tvshow": "ep"
}


class ImdbSpider(object):
    domain = "http://www.imdb.com"

    def __init__(self, title, type="all"):
        self.title = title
        search_type_path = self._get_search_path(type)
        self.search_url = u"{}/find?s={}&q={}".format(self.domain,
                                                      search_type_path,
                                                      self.title)
        self.link_detail = self._scrap_link_detail()
        if not self.link_detail:
            raise Exception()
        page = requests.get(self.link_detail)
        self.tree = html.fromstring(page.content)

    def _get_search_path(self, type):
        return TYPE_SEARCH.get(type) or TYPE_SEARCH["all"]

    def _scrap_link_detail(self):
        page = requests.get(self.search_url)
        tree = html.fromstring(page.content)
        try:
            detail_path = tree.xpath(
                "//td[@class='result_text']/a")[0].items()[0][1]
            return u"{}{}".format(self.domain, detail_path)
        except IndexError:
            raise Exception("No details found from: {}".format(self.title))

    def get_rating(self):
        try:
            return self.tree.xpath("//span[@itemprop='ratingValue']")[
                0].text.strip()
        except IndexError:
            pass

    def get_title(self):
        # Retrieve the original title
        try:
            return self.tree.xpath("//div[@class='originalTitle']")[
                0].text.strip()
        except IndexError:
            pass

    def get_year(self):
        # Retrieve the original title
        try:
            return self.tree.xpath("//span[@id='titleYear']/a")[0].text.strip()
        except IndexError:
            pass
