import pytest
from selene import browser
from selenium import webdriver


@pytest.fixture(scope='function', autouse=True)
def browser_settings():
    browser.config.driver_options = webdriver.ChromeOptions()
    browser.driver.maximize_window()

    yield

    browser.quit()