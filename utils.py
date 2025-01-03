import logging
import time
from collections.abc import Callable

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException, NoSuchElementException

import config
from exceptions import SignInError, NoSignInCredentialsError, NoSignInFieldsError, HTMLElementNotFoundError, \
    FormNotFilledError, URLNotPassedError

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def load_page_and_run_func(driver: WebDriver, page_url: str, func: Callable) -> None:
    if not page_url or page_url == '':
        raise URLNotPassedError(f"Page url for {func.__name__} function not provided")
    load_page(driver, page_url)
    func(driver)


def click_element(driver: WebDriver, element: WebElement, delay: float = 1.0) -> None:
    try:
        if not element.is_displayed():
            driver.execute_script("arguments[0].scrollIntoView(true);", element)

        try:
            ActionChains(driver).move_to_element(element).click().perform()
        except Exception as e:
            logger.warning("ActionChains failed, falling back to JavaScript: %s", e)
            driver.execute_script("arguments[0].click();", element)

        time.sleep(delay)
        logger.debug("Element %s was clicked", element)

    except Exception as e:
        logger.exception("Failed to click element: %s", e)


def save_plays(driver: WebDriver) -> None:
    unique_card_ids = set()
    counter = 0

    cards = driver.find_elements(By.CSS_SELECTOR, f"[id*='{config.CARD_SELECTOR}']")
    logger.info("Play founded - %s", len(cards or ''))

    for card in cards:
        is_duplicate_badge = card.find_elements(By.XPATH, f".//p[text()='{config.DUPLICATE_TEXT_ALERT}']")

        try:
            card_id_element = card.find_element(By.CSS_SELECTOR, config.CARD_ID_SELECTOR)
            card_id = card_id_element.get_attribute(config.CARD_ID_ATTR)
            logger.info("Current Cart ID: %s", card_id)

            if is_duplicate_badge:
                logger.info("Card ID: %s skipped because of duplicate badge", card_id)
                continue

            if card_id is None:
                logger.warning("Unable to find Card ID for card")
                continue

            if card_id in unique_card_ids:
                logger.info("Card ID: %s skipped because of duplicate", card_id)
                continue

            unique_card_ids.add(card_id)

            logger.info("Duplicates not found")

            option_element = card.find_element(By.CSS_SELECTOR, config.OPTIONS_BUTTON_SELECTOR)
            logger.info("Option element found")
            click_element(driver, option_element, config.CLICK_DELAY)

            save_element = card.find_element(By.CSS_SELECTOR, config.SAVE_BUTTON_SELECTOR)
            logger.info("Save element found")
            click_element(driver, save_element, config.CLICK_DELAY)

            counter += 1

        except NoSuchElementException as e:
            logger.exception("Unable to find element in card: %s\n%s", card, e)
        except WebDriverException as e:
            logger.exception("WebDriverException message: %s", e)

    logger.info("Plays saved - %s", counter)


def sign_in(driver: WebDriver) -> None:
    if not (config.LOGIN_FIELD_SELECTOR and config.PASSWORD_FIELD_SELECTOR):
        raise NoSignInFieldsError("Credential fields haven't been found")

    try:
        url_before_signin = driver.current_url
        login_field = driver.find_element(By.ID, config.LOGIN_FIELD_SELECTOR)
        password_field = driver.find_element(By.ID, config.PASSWORD_FIELD_SELECTOR)
    except Exception as e:
        raise HTMLElementNotFoundError("HTML Element not found: %s", e)

    if not (config.LOGIN and config.PASSWORD):
        raise NoSignInCredentialsError("No sign in credentials")

    try:
        login_field.send_keys(config.LOGIN)
        password_field.send_keys(config.PASSWORD)
        password_field.send_keys(Keys.RETURN)
    except Exception as e:
        raise FormNotFilledError("Form not filled: %s", e)

    if url_before_signin == driver.current_url:
        raise SignInError("Unsuccessful attempt to sign in!")

    logger.info("Signed in successfully")
    time.sleep(1)


def load_page(driver: WebDriver, page: str) -> None:
    driver.get(page)
    driver.implicitly_wait(10)
    logger.info("Page '%s' loaded", driver.current_url)


def get_chrome_webdriver() -> WebDriver:
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    return webdriver.Chrome(options=chrome_options)
