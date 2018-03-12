import unittest

from test_KC import KC_Test
from test_no_KC import Not_KC_Test

# get all tests from SearchText and HomePageTest class
kc_test = unittest.TestLoader().loadTestsFromTestCase(KC_Test)
not_KC_test = unittest.TestLoader().loadTestsFromTestCase(Not_KC_Test)

# create a test suite combining search_text and home_page_test
test_suite = unittest.TestSuite([kc_test, not_KC_test])

# run the suite
unittest.TextTestRunner(verbosity=2).run(test_suite)
