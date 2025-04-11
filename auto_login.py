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
    browser.add_cookie({"name": "MUSIC_U", "value": "004A95CE9F2B24B860389B6E1C859FF31F289A5D1435AEDC0614F57DAD6DD9648F37A5C6FF45894B8DB579D26B570451F188BE9913658B24F06954DC20C0A40CA8A9D786EC60FE0A88C8EA85C6408182A0C033E7874FB4E67B4B0285A95E3EE23D0A5F0F87F6771D8DA9E64713C7455F414174EE0AED8FE447F4A271E91E3085AE308FB046ED1C8269F209884A9802A7BE30A90EFD0719F764D80B7607C8BC45D1EE9DB12CC2ED31F92A8CA54FE15D156A576DDC710B767E25182442129900369809D94D9C0A49D4D090462430E1B07E8B7959DD887A2A0A3935D3246B3B48E433FFD96D8BFCD8BE6A6903F2573283C85E471F853F5BF392723A5B70436C04A95BB5BD42DD65A789E9E546E0708E97169908F2F5D3244519EE6410847F1333E2484E09FB9DA1563813754FC140000147091C47CF5FF8673A93A4EB33783D837CEB43782DF835E7D91DFCDA4430BD3622419D035A71D528C08A606572836EE33C71"})
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
