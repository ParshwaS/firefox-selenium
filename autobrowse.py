from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
import os
import contextlib

wait_time = 5

def create_driver():
    chrome_options = webdriver.FirefoxOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--log-level=3")

    with contextlib.redirect_stdout(None):
        driver = webdriver.Firefox(options=chrome_options)
    
    return driver

def is_clickable(element):
    try:
        element.click()
        return True
    except WebDriverException:
        return False

def wait_for_element(driver, element, count):
    if(driver.find_elements_by_css_selector(element) != []):
        if(driver.find_element_by_css_selector(element).is_displayed() and driver.find_element_by_css_selector(element).is_enabled() and is_clickable(driver.find_element_by_css_selector(element))):
            return True
        else:
            time.sleep(.3)
            count += 1
            if(count > wait_time):
                print("Time Limit Exceeded!!")
                return False
            else:
                return wait_for_element(driver, element, count)
    else:
        time.sleep(.3)
        count += 1
        if(count > wait_time):
            print("Time Limit Exceeded!!")
            return False
        else:
            return wait_for_element(driver, element, count)

def wait_for_element_x(driver, element, count):
    if(driver.find_elements_by_xpath(element) != []):
        if(driver.find_element_by_xpath(element).is_displayed() and driver.find_element_by_xpath(element).is_enabled() and is_clickable(driver.find_element_by_xpath(element))):
            return False
        else:
            time.sleep(.3)
            count += 1
            if(count > wait_time):
                print("Time Limit Exceeded!!")
                return True
            else:
                return wait_for_element_x(driver, element, count)
    else:
        time.sleep(.3)
        count += 1
        if(count > wait_time):
            print("Time Limit Exceeded!!")
            return True
        else:
            return wait_for_element_x(driver, element, count)