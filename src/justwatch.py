from os import getenv
from re import sub
from typing import NamedTuple

from dotenv import load_dotenv
from loguru import logger
from selenium.webdriver import Firefox, FirefoxOptions, FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.support.expected_conditions import (
    element_to_be_clickable,
    presence_of_element_located,
)
from selenium.webdriver.support.wait import TimeoutException, WebDriverWait


class WatchOffer(NamedTuple):
    name: str
    url: str
    value: str


class MediaEntry(NamedTuple):
    title: str
    year: str
    watch_options: dict[str, WatchOffer]


class JustWatchApi:
    COOKIES_POPUP_ID = "usercentrics-root"
    COOKIES_ACCEPT_CSS = "button[data-testid=uc-accept-all-button]"
    JUSTWATCH_URL = "https://www.justwatch.com"
    SEARCH_URL = JUSTWATCH_URL + "/{country}/search?q={name}"
    DEFAULT_IMPLICIT_WAIT = 10

    def __init__(self, country: str = "us"):
        logger.info("Setting up Selenium...")
        self.country = country
        load_dotenv()
        firefox_bin = getenv("FIREFOX_BIN")
        firefox_driver = getenv("FIREFOX_DRIVER")
        options = FirefoxOptions()
        options.add_argument("--headless")
        options.add_argument(f"binary_location={firefox_bin}")
        service = FirefoxService(firefox_driver)
        self.driver = Firefox(options=options, service=service)
        self.driver.implicitly_wait(self.DEFAULT_IMPLICIT_WAIT)
        logger.info("Opening JustWatch...")
        self.driver.get(self.JUSTWATCH_URL)
        logger.info("Accepting cookies...")
        self._accept_cookies()
        logger.info("JustWatch ready!")

    def __del__(self):
        self.driver.quit()

    def search(self, name: str) -> list[MediaEntry]:
        logger.info(f"Looking up {name} (country: {self.country})...")
        url = self.SEARCH_URL.format(country=self.country, name=name)
        self.driver.get(url)
        logger.info(f"Parsing response for {name} (country: {self.country})...")
        media_locator = By.CLASS_NAME, "title-list-row__row"
        WebDriverWait(self.driver, 10).until(presence_of_element_located(media_locator))
        return [self._parse_media(entry) for entry in self.driver.find_elements(*media_locator)]

    def _accept_cookies(self):
        try:
            popup_wait = WebDriverWait(self.driver, 10)
            cookie_popup_locator = By.ID, self.COOKIES_POPUP_ID
            cookie_popup = popup_wait.until(presence_of_element_located(cookie_popup_locator))
            shadow = cookie_popup.shadow_root
            button_wait = WebDriverWait(shadow, 10)
            button_locator = By.CSS_SELECTOR, self.COOKIES_ACCEPT_CSS
            button = button_wait.until(element_to_be_clickable(button_locator))
            button.click()
        except TimeoutException:
            pass

    def _parse_media(self, media: WebElement) -> MediaEntry:
        title = media.find_element(By.CLASS_NAME, "header-title").text
        year = sub(r"[)(]", "", media.find_element(By.CLASS_NAME, "header-year").text)
        buybox = media.find_element(By.CLASS_NAME, "buybox__content")
        options = self._parse_options(buybox)
        return MediaEntry(title, year, options)

    def _parse_options(self, buybox: WebElement) -> dict[str, WatchOffer]:
        # Since buybox is loaded, then these elements should be as well.
        # Waiting for no-offer-row slows the API down significantly.
        self.driver.implicitly_wait(0)
        if buybox.find_elements(By.CLASS_NAME, "no-offer-row"):
            return {}
        self.driver.implicitly_wait(self.DEFAULT_IMPLICIT_WAIT)
        return {
            self._parse_option_name(option): self._parse_option(option)
            for option in buybox.find_elements(By.CLASS_NAME, "buybox-row")
        }

    def _parse_option_name(self, option: WebElement) -> str:
        return option.find_element(By.CLASS_NAME, "buybox-row__label").text.capitalize()

    def _parse_option(self, option: WebElement) -> list[WatchOffer]:
        offers_field = option.find_element(By.CLASS_NAME, "buybox-row__offers")
        return [
            WatchOffer(
                offer.find_element(By.TAG_NAME, "img").accessible_name,
                offer.get_attribute("href"),
                offer.find_element(By.CLASS_NAME, "offer__label").text,
            )
            for offer in offers_field.find_elements(By.CLASS_NAME, "offer")
        ]
