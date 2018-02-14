import logging
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.event_firing_webdriver import WebElement
from selenium.webdriver.support.ui import WebDriverWait

from core.tools import timeit


class BaseScraper:
    ROOT_URL = None
    COMPANY_NAME = None
    TIMEOUT = 30  # time for driver waiting while element will be loaded

    def __init__(
            self,
            shared_dict,
            delay,
            executable_path,
            driver_extra_options=None):
        """
        :param shared_dict: multiprocessing.manager.dict
        :param delay: integer delay between requests in seconds
        :param executable_path path of chromedriver located
        :param driver_extra_options: None or tuple with run args like:
        (
            '--incognito',
            '--proxy-server=http://',
            '--headless',
            ...
        )
        """
        options = Options()
        if driver_extra_options:
            for opt in driver_extra_options:
                options.add_argument(opt)

        self.driver = webdriver.Chrome(
            options=options,
            executable_path=executable_path
        )
        self.delay = delay
        self.shared_dict = shared_dict

        # should be overwritten in childs
        self.xpath_map = tuple()

    @timeit
    def setup(self):
        """
        Loads base URL and navigates to page with odds
        """
        while True:
            try:
                self.driver.get(self.ROOT_URL)
                self._navigate_by_xpath()
                return
            except WebDriverException as err:
                logging.error(repr(err))
                continue

    @timeit
    def proceed(self):
        """
        Use this method to wrap self._proceed with timeit decorator
        """
        return self._proceed()

    def _proceed(self):
        """
        Abstract method which should be implemented in all child's,
        and return the struct like:
        {
            country_name1: 'odd1/odd2',
            country_name2: 'odd1/odd2',
            ...
        }
        """
        raise NotImplementedError

    def _navigate_by_xpath(self):
        """
        Click on each element found by xpath.
        """
        for path in self.xpath_map:
            for _ in range(3):
                try:
                    element = self._safe_load_by_xpath(path)
                except TimeoutException:
                    continue
                try:
                    element.click()
                except WebDriverException:
                    # sometimes there are WebDriverExceptions raised when
                    # clickable element not in view
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({inline: 'center'});",
                        element
                    )
                    continue
                else:
                    break

    def pool(self):
        self.setup()
        while True:
            try:
                result = self.proceed()
            except Exception as err:
                logging.error(
                    f'Got {repr(err)} while processing {self.COMPANY_NAME}'
                )
                # if something came wrong better to go home and retry
                self.setup()
            else:
                if not result:
                    continue
                self.shared_dict[self.COMPANY_NAME] = result
                time.sleep(self.delay)

    def _safe_load_by_xpath(self, path: str) -> WebElement:
        """
        Finds by xpath visible element and return it
        :param path: xpath expression
        :return: WebElement object
        """
        return WebDriverWait(self.driver, self.TIMEOUT).until(
            expected_conditions.element_to_be_clickable((By.XPATH, path))
        )
