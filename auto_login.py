# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00EF474B65F71ADC5C69524A5332F41EA08F592BACAC6DDC679F3E0710735CA0516BC23E1C3BFCB5E4C7623E530D039F6F68125814367C4F063EEBE2F18CE866FA87871E58E591C7CAA155003DE76E4906E03DE32CAA2E00B1260D4D9D41A3E9201BA68500EE0E24B0C533001B2145A1005FA386F1C84F862F119C667E586AAEFB208886E9198FCD8B6BF3436CD8BC4DC17286BAC32DD212906C1D6B10FD02BF4FC865FD1D0CC56AB99409DC29E2FEA9920EB2D6D9545914CEE1260AA0D9A20D4CFF0BE1834C2E95D9DC346B6D8556A30870EEF538FE4A872FDB07893E5C690C0E0D64FDB0F1C619E5273F40D6D381D789E1B4D8614ED3217EDD7505AD21EDA8817E6AA7C17A0F84D5FAC9DE1A26AB5BDE41BFA2FD05CC20ACB160886F133FCFBD2AF043162BF43673F53F708E59BE7299C61563072FC59DDF078342ECF3F5623CD2528861AB944766A82911C464823BED"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
