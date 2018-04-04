# -*- coding: utf-8 -*-
from scrapimdb import ImdbSpider


def test_imdb():
    title = "terminator"
    im = ImdbSpider(title)
    assert "The Terminator" == im.get_title()
    float(im.get_rating())
    assert "1984" == im.get_year()
