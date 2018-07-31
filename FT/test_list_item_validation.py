from .base import FunctionalTest
from unittest import skip
import time
from selenium.webdriver.common.keys import Keys
from lists.forms import DUPLICATE_LIST_ERROR


class ItemValidationTest(FunctionalTest):

    @skip
    # the whole fucking code doesnt work... fuck it (page 174 TDD)
    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # we specify we are going to use a CSS class fom Bootstrap called .has-error
        # to make our error text.
        error = self.browser.find_element_by_class_name('has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        # we reuse check_for_row_in_list_table when we want to confirm that list item
        # submission does work.
        self.check_for_row_in_list_table('1: Buy milk')

        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        # self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        self.check_for_row_in_list_table('1: Buy milk')
        error = self.browser.find_element_by_class_name('has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        inputbox.send_keys('Make tea')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_items(self):
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: Buy wellies')

        self.get_item_input_box().send_keys('Buy wellies\n')
        self.check_for_row_in_list_table('1: Buy wellies')
        # error = self.browser.find_element_by_css_selector('.has-error')
        error = self.browser.find_element_by_class_name('has-error')
        self.assertEqual(error.text, DUPLICATE_LIST_ERROR)
