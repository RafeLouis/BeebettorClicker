import logging

import config
from utils import get_webdriver, load_page, sign_in, save_plays

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def lambda_handler(event, context):
    driver = get_webdriver()
    try:
        load_page(driver, config.SIGNIN_PAGE)
        sign_in(driver)
        load_page(driver, config.WORKING_PAGE)
        save_plays(driver)
    except Exception as e:
        logger.error("An error occurred: %s", e)
    finally:
        if driver:
            driver.quit()
            logger.info("Chrome browser closed successfully")

    return {
        "statusCode": 200,
        "body": "Lambda function completed successfully"
    }
