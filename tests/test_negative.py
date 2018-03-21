import time
import unittest

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from selenium_config import get_path


class NegativeTest(unittest.TestCase):
    address_good_KC = ['1724 Beacon Way SE Renton, WA 98058', '1925 N 170th St Shoreline, WA 98133']
    address_bad = ['fjweogrgjrgl;jjegjegjgjlgjjgl;jgljgslj', '3000 Royal Hills Dr SE Renton, WA 98058, apt 1d,  apt 1d', \
                   '3000 Royal Hills Dr SE Renton WA 98058 apt 1d', \
                   '904 Hiawatha Pl S, Seattle, apt 1C, apt 1C, WA 98144', '', \
                   'iosfi iosejfdujfi esofjedsj eofe 9898908 kiefkljkj 9898', \
                   '($(*$(#$*#*%(#@*@*!($(*%$*%(*$*$(**!@(*$@(!*$(*(*($*@$*!(@*$', \
                   '()*(* )(_* )*             )_()()(            )((((              ', \
                   '3000          Royal      Hills      Dr SE Renton         WA 98058       apt 1d       apt 1d'
                   ]
    address_good = ['8105 SE Henderson St Portland, OR 97206']
    zip_good = ['98058', '98053']

    @classmethod
    def setUp(inst):
        options = Options()  # set custom paths
        options.binary_location = get_path().crome_path  # set custom paths
        inst.driver = webdriver.Chrome(chrome_options=options,
                                       executable_path=get_path().webdriver_path, )  # set custom paths
        inst.driver.implicitly_wait(30)
        inst.driver.maximize_window()
        # navigate to the application home page
        inst.driver.get(get_path().app_path)  # get the homepage

    def test_search_by_address_negative(self):
        # self.driver.execute_script("alert('This is an alert');")
        res = True
        for el in self.address_bad:
            self.search_field = self.driver.find_element_by_name('address')  # find_element_by_name
            self.search_field.send_keys(el)  # input address
            self.search_field.submit()  # press search
            if not self.is_element_present(By.CLASS_NAME, "price"):
                res = False
                print("address=", el)
                break
            else:
                time.sleep(1)
                self.driver.implicitly_wait(5)
                self.driver.get(get_path().app_path)
        self.assertTrue(res)

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
