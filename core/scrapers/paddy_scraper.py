from core.scrapers.base_scrapper import BaseScraper


class PaddyScraper(BaseScraper):
    ROOT_URL = 'http://www.paddypower.com/bet'
    COMPANY_NAME = 'PaddyPower'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xpath_map = (
            '//div[@id="newModal"]/img',  # close popup
            '//ul[@id="sitemap"]/li/a[@title="Football Betting"]',
            '//div[@id="main"]/div/ul/li/a[normalize-space()="Outrights"]',
            ('//div[@class="fb-sub-content fb-outrights"]/div/'
             'a[contains(normalize-space(), "World Cup 2018")]')
        )

    def _proceed(self):
        table = self._safe_load_by_xpath('//div[@class="fb-sub-content"]')
        results = {}
        for tab in table.find_elements_by_xpath(
                '//div/span/a[@class="fb-odds-button"]'
        ):
            country, odd = map(
                tab.find_element_by_class_name, ('odds-label', 'odds-value')
            )
            results[country.text] = odd.text

        return results
