# -*- coding: utf-8 -*-

import cloudscraper
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
        search_type_path = TYPE_SEARCH.get(type) or TYPE_SEARCH["all"]
        self.search_url = u"{}/find?s={}&q={}".format(self.domain,
                                                      search_type_path,
                                                      self.title)
        self._link_detail = self._scrap_link_detail()
        self.tree_detail = self._extract_page_content(self._link_detail)

    def get_link(self):
        return self._link_detail

    @staticmethod
    def _extract_page_content(link):
        if not link:
            raise Exception()
        scraper = cloudscraper.create_scraper()
        page = scraper.get(link)
        return html.fromstring(page.text)

    def _scrap_link_detail(self):
        tree = self._extract_page_content(self.search_url)
        try:
            # Get the first url result from imdb search
            #import ipdb; ipdb.set_trace()
            detail_path = tree.xpath(
                "//a[@class='ipc-metadata-list-summary-item__t']")[0].items()[-1][1]
            return u"{}{}".format(self.domain, detail_path)
        except IndexError:
            raise Exception("No details found from: {}".format(self.title))

    def get_rating(self):
        try:
            return self.tree_detail.xpath(
                "///div[contains(@data-testid, 'hero-rating-bar__aggregate-rating__score')]"
                "/span")[0].text.strip()
        except IndexError:
            raise Exception(
                "No rating found from: {}".format(self.title))

    def get_original_title(self):
        # Retrieve the original title
        try:
            orginal_title = self.tree_detail.xpath(
                "//div[contains(@data-testid, "
                "'hero-title-block__original-title')]")[0].text.strip()
        except IndexError:
            raise Exception(
                "No original title found from: {}".format(self.title))
        return orginal_title.split('Original title: ')[1].strip()

    def get_year(self):
        # Retrieve the original title
        try:
            return self.tree_detail.xpath(
                "//ul[contains(@data-testid, "
                "'hero-title-block__metadata')]"
                "/li[@class='ipc-inline-list__item']/a")[0].text.strip()
        except IndexError:
            raise Exception(
                "No year found from: {}".format(self.title))
