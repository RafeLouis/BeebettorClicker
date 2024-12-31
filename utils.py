import logging
import time

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException

import config
from exceptions import SignInError, NoSignInCredentialsError, NoSignInFieldsError, HTMLElementNotFoundError, \
    FormNotFilledError

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def click_element(driver: WebDriver, element: WebElement, delay: float = 1.0) -> None:
    ActionChains(driver).move_to_element(element).click().perform()
    time.sleep(delay)
    logger.debug("Element %s was clicked", element)


def save_plays(driver: WebDriver) -> None:
    counter = 0
    elements = driver.find_elements(By.CSS_SELECTOR, config.OPTIONS_BUTTON_SELECTOR)

    logger.info("%s plays founded", len(elements or ''))

    for option_element in elements:
        try:
            click_element(driver, option_element, config.CLICK_DELAY)

            parent_element = option_element.find_element(By.XPATH, "./parent::div/parent::div")
            save_element = parent_element.find_element(By.CSS_SELECTOR, config.SAVE_BUTTON_SELECTOR)
            click_element(driver, save_element, config.CLICK_DELAY)
            counter += 1
        except WebDriverException as e:
            logger.exception("WebDriverException message: %s", e)

    logger.info("%s plays saved", counter)


def sign_in(driver: WebDriver) -> None:
    url_before_signin = driver.current_url

    if not (config.LOGIN_FIELD_SELECTOR and config.PASSWORD_FIELD_SELECTOR):
        raise NoSignInFieldsError("Credential fields haven't been found")

    try:
        login_field = driver.find_element(By.ID, config.LOGIN_FIELD_SELECTOR)
        password_field = driver.find_element(By.ID, config.PASSWORD_FIELD_SELECTOR)
    except WebDriverException as e:
        raise HTMLElementNotFoundError("HTML Element not found: %s", e)

    if not (config.LOGIN and config.PASSWORD):
        raise NoSignInCredentialsError("No sign in credentials")

    try:
        login_field.send_keys(config.LOGIN)
        password_field.send_keys(config.PASSWORD)
        password_field.send_keys(Keys.RETURN)
    except WebDriverException as e:
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
