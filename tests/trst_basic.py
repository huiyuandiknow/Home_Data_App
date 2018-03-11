import unittest

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium_config import get_path


class HomePageTest(unittest.TestCase):
    address = '1724 Beacon Way SE Renton, WA 98058'

    @classmethod
    def setUp(inst):
        options = Options()
        options.binary_location = get_path().crome_path
        inst.driver = webdriver.Chrome(chrome_options=options, executable_path=get_path().webdriver_path, )
        inst.driver.implicitly_wait(30)
        inst.driver.maximize_window()
        # navigate to the application home page
        inst.driver.get(get_path().app_path)

    def test_search_by_name(self):
        # get the search textbox
        self.search_field = self.driver.find_element_by_name('address')
        # enter search keyword and submit
        self.search_field.send_keys(self.address)
        self.search_field.submit()
        self.driver.implicitly_wait(5)
        val = (self.driver.find_element_by_class_name("price"))
        val2 = val.get_attribute('innerHTML')
        res = True
        try:
            int(val2)
        except:
            res = False
            print("val=", res)
        self.assertTrue(res)

        self.assertTrue(int(val.get_attribute('innerHTML')))

    @classmethod
    def tearDown(inst):
        # close the browser window
        inst.driver.quit()

    def is_element_present(self, how, what):
        """
        Helper method to confirm the presence of an element on page
        :params how: By locator type
        :params what: locator value
        """
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException:
            return False
        return True


if __name__ == '__main__':
    unittest.main(verbosity=2)
