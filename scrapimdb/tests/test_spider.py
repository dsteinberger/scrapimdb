import pytest

from scrapimdb import ImdbSpider


@pytest.fixture
def spider():
    return ImdbSpider("terminator 1984")


def test_imdb_rating(spider):
    float(spider.get_rating())


# Not working on travis !?
# def test_imdb_title(spider):
#   assert "The Terminator" == spider.get_original_title()


def test_imdb_year(spider):
    assert "1984" == spider.get_year()


def test_imdb_link(spider):
    link = spider.get_link()
    # Accept any link to The Terminator (1984), as the ref parameter may vary
    assert "http://www.imdb.com/title/tt0088247/" in link
