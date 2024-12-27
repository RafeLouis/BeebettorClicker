import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

SIGNIN_PAGE = os.getenv("SIGNIN_PAGE")
WORKING_PAGE = os.getenv("WORKING_PAGE")

OPTIONS_BUTTON_SELECTOR = os.getenv("OPTIONS_BUTTON_SELECTOR")
SAVE_BUTTON_SELECTOR = os.getenv("SAVE_BUTTON_SELECTOR")

LOGIN_FIELD_SELECTOR = os.getenv("LOGIN_FIELD_SELECTOR")
PASSWORD_FIELD_SELECTOR = os.getenv("PASSWORD_FIELD_SELECTOR")

LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")

CLICK_DELAY = float(os.getenv("CLICK_DELAY"))

CLICK_FREQUENCY_IN_MIN = int(os.getenv("CLICK_FREQUENCY_IN_MIN"))
