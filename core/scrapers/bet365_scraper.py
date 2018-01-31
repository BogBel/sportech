import re
import operator

from core.scrapers.base_scrapper import BaseScraper


class Bet365Scrapper(BaseScraper):
    ROOT_URL = 'https://mobile.bet365.com/'
    COMPANY_NAME = 'Bet365'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xpath_map = (
            '//div[@id="IconSplash"]/div/div/div[text()="Soccer"]',
            '//div[@id="Tabs"]/ul/li/span[text()="Outrights"]',
            ('//div[@class="Outrights"]/div/div/div/'
             'span[text()="World Cup 2018"]'),
        )

    def _proceed(self):
        table = self._safe_load_by_xpath(
            '//div[@id="Coupon"]/div/div[@class="eventWrapper"]'
        )
        string_odds = map(
            operator.attrgetter('text'),
            table.find_elements_by_xpath('//span[@class="opp"]'),
        )
        regex = re.compile('(?P<country>^.*?)\s+(?P<odd>\d+\/\d+)')
        return {
                odd.group('country'): odd.group('odd')
                for odd in map(regex.search, string_odds)
        }
