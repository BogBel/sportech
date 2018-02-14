from core.scrapers.base_scrapper import BaseScraper


class PaddyScraper(BaseScraper):
    ROOT_URL = 'http://www.paddypower.com/bet'
    COMPANY_NAME = 'PaddyPower'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xpath_map = (
            '//div[@class="modal"]//button',  # close popup
            '//a[@ng-href="/football"]',
            '//a[@ng-href="/football?tab=tournaments"]',
            '//a[@href="/football/fifa-world-cup-2018"]',
            '//a[@ng-href="/football/fifa-world-cup-2018?tab=outrights"]',
            '//button[normalize-space()="Show More"]'
        )

    def _proceed(self):
        table = self._safe_load_by_xpath(
            '//div[@class="grid outright-item-grid-list__row"]'
        )
        results = {}
        for tab in table.find_elements_by_xpath(
                '//outright-item/div'
        ):
            country, odd = map(
                tab.find_element_by_tag_name, ('p', 'button')
            )
            results[country.text] = odd.text

        return results
