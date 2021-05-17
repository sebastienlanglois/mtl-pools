from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import json
from selenium.webdriver.firefox.options import Options
from config import Config
from sys import argv


def get_page_id(table, schedule):
    print('get page')
    page_id = None
    rows = table.find_elements(By.TAG_NAME, "tr") # get all of the rows in the table
    for row in rows[1:]:
        # Get the columns (all the column 2)
        if row.text.find(schedule) != -1:
            page_id = row.get_attribute('id')
    return page_id


if __name__ == "__main__":

    if Config.ready_to_register:

        username, password = argv[1:]

        options = Options()
        options.headless = False

        driver = webdriver.Firefox(options=options)
        driver.get(Config.website_url)
        time.sleep(8)
        driver.find_element_by_id("u2000_btnSignIn").click()
        time.sleep(3)
        driver.find_element_by_id("loginForm:username").send_keys(username)
        driver.find_element_by_id("loginForm:password").send_keys(password)
        time.sleep(2)
        driver.find_element_by_id("loginForm:loginButton").click()
        time.sleep(10)

        for attempt in range(0, 100):
            response = driver.get((Config.table_activities_url + json.dumps(Config.params)))
            time.sleep(5)
            table = driver.find_element_by_id("u5200_tableTableActivitySearch")
            time.sleep(2)
            page_id = get_page_id(table, Config.schedule)

            if page_id is not None:
                print('finding activity...')
                print(os.path.join(Config.specific_activity_prefix_url,
                                        page_id))
                driver.get(os.path.join(Config.specific_activity_prefix_url,
                                        page_id))
                time.sleep(3)
                try:
                    driver.find_element_by_id("u5200_btnRegisterSecond").click()
                    time.sleep(3)
                    try:
                        driver.find_element_by_id("u3600_btnRemove0")
                    except:
                        driver.find_element_by_id("u3600_btnSelect0").click()
                        time.sleep(3)
                    driver.find_element_by_id("u3600_btnCartMemberCheckout").click()
                    time.sleep(2)
                    driver.find_element_by_id("u3600_btnCartShoppingCompleteStep").click()
                    time.sleep(2)
                    driver.find_element_by_id("u3600_chkElectronicPaymentCondition").click()
                    time.sleep(2)
                    driver.find_element_by_id("u3600_btnCartPaymentCompleteStep").click()
                    break
                except:
                    print('attempt #{} failed'.format(attempt))
                    pass
            time.sleep(10)

        driver.quit()
