"""Complete test coverage for ImdbSpider"""

import pytest
from lxml import html
from unittest.mock import Mock, MagicMock

from scrapimdb import ImdbSpider


@pytest.fixture
def mock_search_response():
    """Mock HTML response for IMDB search page"""
    return """
    <html>
        <body>
            <section data-testid="find-results-section-title">
                <ul class="ipc-metadata-list">
                    <li class="ipc-metadata-list-summary-item">
                        <a href="/title/tt0088247/?ref_=fn_i_1">
                            <span class="ipc-metadata-list-summary-item__t">The Terminator</span>
                        </a>
                        <span class="sc-3eaf0513-7 hmmeot cli-title-metadata-item">1984</span>
                        <span class="sc-3eaf0513-7 hmmeot cli-title-metadata-item">1h 47m</span>
                    </li>
                </ul>
            </section>
        </body>
    </html>
    """


@pytest.fixture
def mock_detail_response():
    """Mock HTML response for IMDB detail page"""
    return """
    <html>
        <body>
            <div data-testid="hero-rating-bar__aggregate-rating__score">
                <span>8.1</span>
            </div>
            <a href="/title/tt0088247/releaseinfo/?ref_=tt_ov_rdat">1984</a>
            <div data-testid="hero-title-block__original-title">
                Original title: The Terminator
            </div>
        </body>
    </html>
    """


@pytest.fixture
def mock_video_search_response():
    """Mock search response with Video results (commercials, etc.)"""
    return """
    <html>
        <body>
            <section data-testid="find-results-section-title">
                <ul class="ipc-metadata-list">
                    <li class="ipc-metadata-list-summary-item">
                        <a href="/title/tt30270541/?ref_=fn_i_1"></a>
                        <span class="sc-3eaf0513-4 jptOTt cli-title-type-data">Video</span>
                        <span class="sc-3eaf0513-7 hmmeot cli-title-metadata-item">1984</span>
                    </li>
                    <li class="ipc-metadata-list-summary-item">
                        <a href="/title/tt0088247/?ref_=fn_i_2"></a>
                        <span class="sc-3eaf0513-7 hmmeot cli-title-metadata-item">1984</span>
                        <span class="sc-3eaf0513-7 hmmeot cli-title-metadata-item">1h 47m</span>
                    </li>
                </ul>
            </section>
        </body>
    </html>
    """


@pytest.fixture
def mock_empty_search_response():
    """Mock empty search response"""
    return """
    <html>
        <body>
            <section data-testid="find-results-section-title">
                <ul class="ipc-metadata-list">
                </ul>
            </section>
        </body>
    </html>
    """


class TestImdbSpiderErrors:
    """Test error cases for full coverage"""

    def test_no_results_found(self, mocker, mock_empty_search_response):
        """Test exception when no search results are found"""
        mock_scraper = MagicMock()
        mock_page = Mock()
        mock_page.text = mock_empty_search_response
        mock_scraper.get.return_value = mock_page

        mocker.patch("cloudscraper.create_scraper", return_value=mock_scraper)

        with pytest.raises(Exception, match="No details found from: nonexistent"):
            ImdbSpider("nonexistent")

    def test_no_title_section_found(self, mocker):
        """Test exception when title section is not found"""
        mock_scraper = MagicMock()
        mock_page = Mock()
        mock_page.text = "<html><body></body></html>"
        mock_scraper.get.return_value = mock_page

        mocker.patch("cloudscraper.create_scraper", return_value=mock_scraper)

        with pytest.raises(Exception, match="No details found from: test"):
            ImdbSpider("test")

    def test_no_title_link_in_result_item(self, mocker):
        """Test exception when result item has no title link"""
        # Create response with item but no link to /title/
        no_link_response = """
        <html>
            <body>
                <section data-testid="find-results-section-title">
                    <ul class="ipc-metadata-list">
                        <li class="ipc-metadata-list-summary-item">
                            <a href="/name/nm0000000/">Some Name</a>
                            <span>Some text</span>
                        </li>
                    </ul>
                </section>
            </body>
        </html>
        """
        mock_scraper = MagicMock()
        mock_page = Mock()
        mock_page.text = no_link_response
        mock_scraper.get.return_value = mock_page

        mocker.patch("cloudscraper.create_scraper", return_value=mock_scraper)

        with pytest.raises(Exception, match="No details found from: test"):
            ImdbSpider("test")

    def test_empty_link_in_extract_page_content(self):
        """Test exception when link is empty in _extract_page_content"""
        with pytest.raises(Exception):
            ImdbSpider._extract_page_content("")

    def test_none_link_in_extract_page_content(self):
        """Test exception when link is None in _extract_page_content"""
        with pytest.raises(Exception):
            ImdbSpider._extract_page_content(None)

    def test_rating_not_found(self, mocker, mock_search_response):
        """Test exception when rating element is not found"""
        # Mock search response
        mock_scraper = MagicMock()
        search_page = Mock()
        search_page.text = mock_search_response

        # Mock detail response without rating
        detail_page = Mock()
        detail_page.text = "<html><body></body></html>"

        mock_scraper.get.side_effect = [search_page, detail_page]
        mocker.patch("cloudscraper.create_scraper", return_value=mock_scraper)

        spider = ImdbSpider("test")

        with pytest.raises(Exception, match="No rating found from: test"):
            spider.get_rating()

    def test_year_not_found(self, mocker, mock_search_response):
        """Test exception when year element is not found"""
        # Mock search response
        mock_scraper = MagicMock()
        search_page = Mock()
        search_page.text = mock_search_response

        # Mock detail response without year
        detail_page = Mock()
        detail_page.text = "<html><body></body></html>"

        mock_scraper.get.side_effect = [search_page, detail_page]
        mocker.patch("cloudscraper.create_scraper", return_value=mock_scraper)

        spider = ImdbSpider("test")

        with pytest.raises(Exception, match="No year found from: test"):
            spider.get_year()

    def test_original_title_not_found(self, mocker, mock_search_response):
        """Test exception when original title element is not found"""
        # Mock search response
        mock_scraper = MagicMock()
        search_page = Mock()
        search_page.text = mock_search_response

        # Mock detail response without original title
        detail_page = Mock()
        detail_page.text = "<html><body></body></html>"

        mock_scraper.get.side_effect = [search_page, detail_page]
        mocker.patch("cloudscraper.create_scraper", return_value=mock_scraper)

        spider = ImdbSpider("test")

        with pytest.raises(Exception, match="No original title found from: test"):
            spider.get_original_title()


class TestImdbSpiderSuccess:
    """Test successful cases for full coverage"""

    def test_get_original_title(self, mocker, mock_search_response, mock_detail_response):
        """Test get_original_title method"""
        mock_scraper = MagicMock()
        search_page = Mock()
        search_page.text = mock_search_response
        detail_page = Mock()
        detail_page.text = mock_detail_response

        mock_scraper.get.side_effect = [search_page, detail_page]
        mocker.patch("cloudscraper.create_scraper", return_value=mock_scraper)

        spider = ImdbSpider("terminator")
        original_title = spider.get_original_title()

        assert original_title == "The Terminator"

    def test_search_type_movie(self, mocker, mock_search_response, mock_detail_response):
        """Test ImdbSpider with type='movie'"""
        mock_scraper = MagicMock()
        search_page = Mock()
        search_page.text = mock_search_response
        detail_page = Mock()
        detail_page.text = mock_detail_response

        mock_scraper.get.side_effect = [search_page, detail_page]
        mocker.patch("cloudscraper.create_scraper", return_value=mock_scraper)

        spider = ImdbSpider("terminator", type="movie")

        assert "s=tt" in spider.search_url
        assert spider.get_link() == "http://www.imdb.com/title/tt0088247/"

    def test_search_type_tvshow(self, mocker, mock_search_response, mock_detail_response):
        """Test ImdbSpider with type='tvshow'"""
        mock_scraper = MagicMock()
        search_page = Mock()
        search_page.text = mock_search_response
        detail_page = Mock()
        detail_page.text = mock_detail_response

        mock_scraper.get.side_effect = [search_page, detail_page]
        mocker.patch("cloudscraper.create_scraper", return_value=mock_scraper)

        spider = ImdbSpider("breaking bad", type="tvshow")

        assert "s=ep" in spider.search_url

    def test_search_type_invalid_defaults_to_all(
        self, mocker, mock_search_response, mock_detail_response
    ):
        """Test ImdbSpider with invalid type defaults to 'all'"""
        mock_scraper = MagicMock()
        search_page = Mock()
        search_page.text = mock_search_response
        detail_page = Mock()
        detail_page.text = mock_detail_response

        mock_scraper.get.side_effect = [search_page, detail_page]
        mocker.patch("cloudscraper.create_scraper", return_value=mock_scraper)

        spider = ImdbSpider("test", type="invalid")

        assert "s=all" in spider.search_url

    def test_video_filtering(self, mocker, mock_video_search_response, mock_detail_response):
        """Test that Video results are filtered in favor of feature films"""
        mock_scraper = MagicMock()
        search_page = Mock()
        search_page.text = mock_video_search_response
        detail_page = Mock()
        detail_page.text = mock_detail_response

        mock_scraper.get.side_effect = [search_page, detail_page]
        mocker.patch("cloudscraper.create_scraper", return_value=mock_scraper)

        spider = ImdbSpider("terminator")

        # Should select the second result (with duration) instead of the first (Video)
        assert "tt0088247" in spider.get_link()

    def test_fallback_to_first_item(self, mocker, mock_detail_response):
        """Test fallback to first item when no filtering criteria match"""
        # Create a response with only video items (no duration)
        only_videos = """
        <html>
            <body>
                <section data-testid="find-results-section-title">
                    <ul class="ipc-metadata-list">
                        <li class="ipc-metadata-list-summary-item">
                            <a href="/title/tt12345/?ref_=fn_i_1"></a>
                            <span class="sc-3eaf0513-4 jptOTt cli-title-type-data">Video</span>
                        </li>
                    </ul>
                </section>
            </body>
        </html>
        """

        mock_scraper = MagicMock()
        search_page = Mock()
        search_page.text = only_videos
        detail_page = Mock()
        detail_page.text = mock_detail_response

        mock_scraper.get.side_effect = [search_page, detail_page]
        mocker.patch("cloudscraper.create_scraper", return_value=mock_scraper)

        spider = ImdbSpider("test")

        # Should fallback to first item
        assert "tt12345" in spider.get_link()
