from core.scrapers.base_scrapper import BaseScraper


class SkybetScraper(BaseScraper):
    # skybet has root url with selected sport, because there was no response
    # while loading skybet.com in headless mode.
    ROOT_URL = 'https://m.skybet.com/football'
    COMPANY_NAME = 'SkyBet'
    DELAY = 180  # because of proxy

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xpath_map = (
            ('//ul[@class="scrolling-nav__tablist"]/li/'
             'a[text()="Competitions"]'),
            '//div[@id="competitions"]//span[text()="World Cup 2018"]',
            ('//table[@class="market-table toggle-market"]/thead/tr/th/'
             'a[@data-toggle-tab="competitions-world-cup-2018-outrights"]'),
            ('//table[@class="market-table competitions-world-cup-2018 '
             'competitions-world-cup-2018-outrights"]/tbody/tr/td/'
             'a/b/span[text()="World Cup 2018 Winner"]'),
        )

    def _proceed(self):
        table = self._safe_load_by_xpath(
            '//div[@id="page-content"]//ul/li'
        )
        zipped = zip(
            table.find_elements_by_xpath('//div[@class="title_1nskdmh"]'),
            table.find_elements_by_xpath('//span[@class="priceInner_14t1nf5"]')
        )
        results = {country.text: odd.text for country, odd in zipped}
        return results

