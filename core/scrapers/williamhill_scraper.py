from core.scrapers.base_scrapper import BaseScraper


class WilliamScrapper(BaseScraper):
    ROOT_URL = (
        'http://sports.williamhill.com/bet/en-gb?'
        'time_zone=29&'
        'action=SetCustTZone&'
        'def_time_zone=0'
    )  # pass timezone in params to avoid popup with TZ selection

    COMPANY_NAME = 'WilliamHill'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xpath_map = (
            '//div[@id="mainNavHolder"]/div/ul/li/a[@id="football"]',
            '//ul[@class="matrixB"]/li/ul/li/a[text()="World Cup 2018"]',
            ('//ul[@class="outrightList"]/li/'
             'a[normalize-space()="World Cup 2018 - Outright"]'),
        )

    def _proceed(self):
        table = self._safe_load_by_xpath(
            '//table[@class="tableData"]'
        )
        divs = table.find_elements_by_xpath(
            '//td[@scope="col"]/div'
        )
        results = dict()
        for div in divs:
            country, price = map(
                div.find_element_by_class_name,
                ('eventselection', 'eventprice')
            )
            results[country.text] = price.text
        return results
