import time
import logging

import config
from utils import get_webdriver, load_page, sign_in, save_plays

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def main():
    logger.info("App started successfully")
    driver = get_webdriver()
    sleep_time = config.CLICK_FREQUENCY_IN_MIN * 3600

    try:
        load_page(driver, config.SIGNIN_PAGE)
        sign_in(driver)

        while True:
            load_page(driver, config.WORKING_PAGE)
            save_plays(driver)
            logger.info("Sleep for %s m", config.CLICK_FREQUENCY_IN_MIN)
            time.sleep(sleep_time)
    except Exception as e:
        logger.error("An error occurred: %s", e)
    finally:
        if driver:
            driver.quit()
            logger.info("Chrome browser closed successfully")


if __name__ == "__main__":
    main()
