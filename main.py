import logging
import sys

import config
from exceptions import URLNotPassedError
from utils import get_chrome_webdriver, load_page, sign_in, save_plays

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("App started successfully")
    driver = get_chrome_webdriver()

    try:
        if not config.SIGNIN_PAGE:
            raise URLNotPassedError("Sign in page url not provided")
        load_page(driver, config.SIGNIN_PAGE)
        sign_in(driver)

        if not config.WORKING_PAGE:
            raise URLNotPassedError("Working page url not provided")
        load_page(driver, config.WORKING_PAGE)
        save_plays(driver)
    except Exception as e:
        logger.error("An error occurred: %s", e)
        sys.exit(1)
    else:
        logger.info("App completed successfully")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
