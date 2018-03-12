import time
import unittest

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

from selenium_config import get_path


class Not_KC_Test(unittest.TestCase):
    address_good_KC = ['1724 Beacon Way SE Renton, WA 98058', '1925 N 170th St Shoreline, WA 98133']
    address_bad = ['fjweogrgjrgl;jjegjegjgjlgjjgl;jgljgslj']
    address_good = ['8105 SE Henderson St Portland, OR 97206', '439 Franklin St Mountain View, CA 94041']
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

    def test_search_by_address(self):
        res = True
        for el in self.address_good:
            self.search_field = self.driver.find_element_by_name('address')  # find_element_by_name
            self.search_field.send_keys(el)  # input address
            self.search_field.submit()  # press search
            val = (self.driver.find_element_by_class_name("price"))  # find_element_by_class_name
            val2 = val.get_attribute('innerHTML')  # get text from current element
            flag = True
            try:
                int(val2)  # if val2 is integer -- it is good
            except:
                flag = False
                print("address=", el, " val=", val2)
            if not flag:
                res = False
                break
            else:
                self.driver.execute_script("window.scrollTo(0, 540)")  # scroll down
                if self.is_zillow():  # if we found a zillow word -- it is ok
                    time.sleep(5)
                    self.driver.implicitly_wait(5)
                    self.driver.get(get_path().app_path)
                else:
                    res = False
                    break
        self.assertTrue(res)

    def is_model(self):
        self.search_fields = self.driver.find_elements_by_class_name('list-group-item')
        for el in self.search_fields:
            li = str(el.get_attribute('innerHTML'))
            # print(li)
            if 'USED ZIP' in li:
                # print(li)
                if 'model' in li:
                    return True
                else:
                    print('sourse=', li)
                    return False

    def is_zillow(self):
        self.search_fields = self.driver.find_elements_by_class_name('list-group-item')
        for el in self.search_fields:
            li = str(el.get_attribute('innerHTML'))
            if 'USED ZIP' in li:
                # print(li)
                if 'zillow' in li:
                    return True
                else:
                    print('sourse=', li)
                    return False

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
