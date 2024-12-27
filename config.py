import os

# SIGNIN_PAGE = os.getenv("SIGNIN_PAGE")
# WORKING_PAGE = os.getenv("WORKING_PAGE")
#
# OPTIONS_BUTTON_SELECTOR = os.getenv("OPTIONS_BUTTON_SELECTOR")
# SAVE_BUTTON_SELECTOR = os.getenv("SAVE_BUTTON_SELECTOR")
#
# LOGIN_FIELD_SELECTOR = os.getenv("LOGIN_FIELD_SELECTOR")
# PASSWORD_FIELD_SELECTOR = os.getenv("PASSWORD_FIELD_SELECTOR")

LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")

CLICK_DELAY = float(os.getenv("CLICK_DELAY"))

SIGNIN_PAGE = "https://beebettor.com/users/sign_in"
WORKING_PAGE = "https://beebettor.com/ev"

OPTIONS_BUTTON_SELECTOR = '[data-action="click->evresult#toggleOptions"]'
SAVE_BUTTON_SELECTOR = '[data-action="click->evresult#savePlay"]'

LOGIN_FIELD_SELECTOR = 'user_email'
PASSWORD_FIELD_SELECTOR = 'user_password'
