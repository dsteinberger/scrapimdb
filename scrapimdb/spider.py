import cloudscraper
from lxml import html

TYPE_SEARCH = {"all": "all", "movie": "tt", "tvshow": "ep"}


class ImdbSpider:
    domain = "http://www.imdb.com"

    def __init__(self, title, type="all"):
        self.title = title
        search_type_path = TYPE_SEARCH.get(type) or TYPE_SEARCH["all"]
        self.search_url = f"{self.domain}/find?s={search_type_path}&q={self.title}"
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
            # First, find the title results section
            section = tree.xpath("//section[@data-testid='find-results-section-title']")
            if not section:
                raise IndexError("No title section found")

            # Get all result items
            items = section[0].xpath(
                ".//li[contains(@class, 'ipc-metadata-list-summary-item')]"
            )
            if not items:
                raise IndexError("No result items found")

            # Filter to find the best match (avoid Videos, prefer feature films)
            selected_item = None
            for item in items:
                # Check if this is a Video (commercial, trailer, etc.)
                video_type = item.xpath(
                    ".//span[contains(@class, 'cli-title-type-data') and contains(text(), 'Video')]"
                )

                # Get duration to check if it's a feature film
                duration_span = item.xpath(
                    ".//span[contains(@class, 'cli-title-metadata')]"
                )
                has_duration = False
                for span in duration_span:
                    text = span.text_content().strip()
                    # Check for hour-minute format (e.g., "1h 47m" or just "107m")
                    if "h" in text or (text.endswith("m") and len(text) > 3):
                        has_duration = True
                        break

                # Prefer items that are NOT videos OR have a proper duration
                if not video_type or has_duration:
                    selected_item = item
                    break

            # If no filtered item found, fall back to first item
            if selected_item is None:
                selected_item = items[0]

            # Get the link from the selected item
            link = selected_item.xpath(".//a[contains(@href, '/title/')]")
            if not link:
                raise IndexError("No title link found")

            # Extract the href and clean it (remove query params)
            href = link[0].get("href", "")
            detail_path = href.split("?")[0] if "?" in href else href

            return f"{self.domain}{detail_path}"
        except IndexError:
            raise Exception(f"No details found from: {self.title}") from None

    def get_rating(self):
        try:
            return self.tree_detail.xpath(
                "///div[contains(@data-testid, 'hero-rating-bar__aggregate-rating__score')]"
                "/span"
            )[0].text.strip()
        except IndexError:
            raise Exception(f"No rating found from: {self.title}") from None

    def get_original_title(self):
        # Retrieve the original title
        try:
            orginal_title = self.tree_detail.xpath(
                "//div[contains(@data-testid, " "'hero-title-block__original-title')]"
            )[0].text.strip()
        except IndexError:
            raise Exception(f"No original title found from: {self.title}") from None
        return orginal_title.split("Original title: ")[1].strip()

    def get_year(self):
        # Retrieve the year from the release info link
        try:
            return self.tree_detail.xpath(
                "//a[contains(@href, '/releaseinfo/?ref_=tt_ov')]"
            )[0].text.strip()
        except IndexError:
            raise Exception(f"No year found from: {self.title}") from None
