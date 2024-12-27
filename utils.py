import logging
import time

from tempfile import mkdtemp
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import config


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def click_element(driver, element, delay=1.0):
    ActionChains(driver).move_to_element(element).click().perform()
    time.sleep(delay)


def save_plays(driver):
    for option_element in driver.find_elements(By.CSS_SELECTOR, config.OPTIONS_BUTTON_SELECTOR):
        click_element(driver, option_element, config.CLICK_DELAY)

        parent_element = option_element.find_element(By.XPATH, "./parent::div/parent::div")
        save_element = parent_element.find_element(By.CSS_SELECTOR, config.SAVE_BUTTON_SELECTOR)
        click_element(driver, save_element, config.CLICK_DELAY)


def sign_in(driver):
    login_field = driver.find_element(By.ID, config.LOGIN_FIELD_SELECTOR)
    password_field = driver.find_element(By.ID, config.PASSWORD_FIELD_SELECTOR)

    login_field.send_keys(config.LOGIN)
    password_field.send_keys(config.PASSWORD)
    password_field.send_keys(Keys.RETURN)
    time.sleep(1)
    logger.info("Signed in successfully")


def load_page(driver, page):
    driver.get(page)
    driver.implicitly_wait(10)
    logger.info("Page '%s' loaded", page)


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
