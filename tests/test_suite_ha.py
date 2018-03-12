import unittest

from test_KC import KcTest
from test_negative import NegativeTest
from test_no_KC import NotKcTest

# get all tests from SearchText and HomePageTest class
kc_test = unittest.TestLoader().loadTestsFromTestCase(KcTest)
not_KC_test = unittest.TestLoader().loadTestsFromTestCase(NotKcTest)
negative_test = unittest.TestLoader().loadTestsFromTestCase(NegativeTest)

# create a test suite combining search_text and home_page_test
test_suite = unittest.TestSuite([kc_test, not_KC_test, negative_test])

# run the suite
unittest.TextTestRunner(verbosity=2).run(test_suite)
