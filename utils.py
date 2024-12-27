import logging
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import config
from exceptions import SignInError

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def click_element(driver, element, delay=1.0):
    ActionChains(driver).move_to_element(element).click().perform()
    time.sleep(delay)
    logger.debug("Element %s was clicked", element)


def save_plays(driver):
    counter = 0
    elements = driver.find_elements(By.CSS_SELECTOR, config.OPTIONS_BUTTON_SELECTOR)

    logger.info("%s plays founded", len(elements or ''))

    for option_element in elements:
        click_element(driver, option_element, config.CLICK_DELAY)

        parent_element = option_element.find_element(By.XPATH, "./parent::div/parent::div")
        save_element = parent_element.find_element(By.CSS_SELECTOR, config.SAVE_BUTTON_SELECTOR)
        click_element(driver, save_element, config.CLICK_DELAY)
        counter += 1

    logger.info("%s plays saved", counter)


def sign_in(driver):
    url_before_signin = driver.current_url

    login_field = driver.find_element(By.ID, config.LOGIN_FIELD_SELECTOR)
    password_field = driver.find_element(By.ID, config.PASSWORD_FIELD_SELECTOR)

    login_field.send_keys(config.LOGIN)
    password_field.send_keys(config.PASSWORD)
    password_field.send_keys(Keys.RETURN)

    if url_before_signin == driver.current_url:
        logger.exception("Unsuccessful attempt to sign in!")
        raise SignInError

    logger.info("Signed in successfully")
    time.sleep(1)


def load_page(driver, page):
    driver.get(page)
    driver.implicitly_wait(10)
    logger.info("Page '%s' loaded", driver.current_url)


def get_webdriver():
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--disable-dev-tools")
    # chrome_options.add_argument("--no-zygote")
    # chrome_options.add_argument("--single-process")
    # chrome_options.add_argument(f"--user-data-dir={mkdtemp()}")
    # chrome_options.add_argument(f"--data-path={mkdtemp()}")
    # chrome_options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    # chrome_options.add_argument("--remote-debugging-pipe")
    # chrome_options.add_argument("--verbose")

    driver = webdriver.Chrome(options=chrome_options)

    return driver
