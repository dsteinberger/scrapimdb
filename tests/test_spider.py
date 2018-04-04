# -*- coding: utf-8 -*-
import pytest
from scrapimdb import ImdbSpider


@pytest.fixture
def spider():
    return ImdbSpider("terminator")


def test_imdb_rating(spider):
    float(spider.get_rating())

# Not working only on travis !?
# def test_imdb_title(spider):
#     assert "The Terminator" == spider.get_original_title()


def test_imdb_year(spider):
    assert "1984" == spider.get_year()
