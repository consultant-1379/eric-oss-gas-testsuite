#!/usr/bin/python
import sys
import unittest
import requests
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pyshadow.main import Shadow

productName="Ericsson Orchestrator"

class TestGas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        opts = FirefoxOptions()
        opts.add_argument("--headless")
        cls.driver = webdriver.Firefox(options=opts)
        cls.driver.get(cls.URL)

        try:
            TestGas.put_key_in_element(cls.driver, "//*[@id='username']", cls.USERNAME)
            TestGas.put_key_in_element(cls.driver, "//*[@id='password']", cls.PASSWORD)
            cls.driver.find_element_by_xpath("//*[@id='kc-login-input']").click()
        except NoSuchElementException:
            raise RuntimeError("Login page not found")

        print("# start waiting", flush=True)
        cls.shadow = Shadow(cls.driver)
        cls.shadow.set_explicit_wait(15, 2)
        print("# end waiting", flush=True)

        # wait until one of the latest elements is loaded
        # IDUN-61450: not the title because it appear much earlier
        try:
            WebDriverWait(cls.driver, 20).until(EC.visibility_of_element_located((By.TAG_NAME, 'eui-container')))
        except TimeoutException:
            raise RuntimeError("Timeout exceeded while waiting for element 'eui-container' - perhaps wrong username/password ?")

    def test_Find_SystemBar(self):
        assert self.shadow.find_element("#SysBar-container") is not None
        print("#SysBar-container found")

    def test_Find_AppBar_menu(self):
        assert self.shadow.find_element("#menu-toggle") is not None
        print("#AppBar-menu-toggle found")

    def test_Find_Products(self):
        assert self.shadow.find_element(".groupName") is not None
        print("products found")

    def test_App1_deployed_in_container_gas(self):
        retry = 0
        element = None

        while (not element) and (retry < 25):
            element = self.find_eo_button_in_elements_list(self.shadow.find_elements("e-custom-layout-card"))
            time.sleep(1)
            retry += 1

        if element:
            self.assertIn(productName, element.text)
            print("App " + productName + " found in " + str(retry) + " retries")
        else:
            self.fail(productName + " Not Found! ")

    @classmethod
    def tearDownClass(cls):
        print("tearDownClass")
        cls.driver.close()

    @staticmethod
    def find_eo_button_in_elements_list(elements):
        for element in elements:
            print(element.text)
            if element.text.__contains__(productName):
                return element

    @staticmethod
    def put_key_in_element(driver, xpath, value):
        elem = driver.find_element_by_xpath(xpath)
        elem.clear()
        elem.send_keys(value)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        TestGas.PASSWORD = sys.argv.pop()
        TestGas.USERNAME = sys.argv.pop()
        TestGas.URL = sys.argv.pop()
    unittest.main(verbosity=2)
