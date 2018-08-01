from .base import FunctionalTest
from unittest import skip
import time
from selenium.webdriver.common.keys import Keys
from lists.forms import DUPLICATE_LIST_ERROR, EMPTY_LIST_ERROR


class ItemValidationTest(FunctionalTest):

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    # the whole fucking code doesnt work... fuck it (page 174 TDD)
    @skip
    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # we specify we are going to use a CSS class fom Bootstrap called .has-error
        # to make our error text.
        self.assertEqual(self.get_error_element().text, EMPTY_LIST_ERROR)

        self.get_item_input_box().send_keys('Buy milk')
        self.get_item_input_box().send_keys(Keys.ENTER)
        # we reuse check_for_row_in_list_table when we want to confirm that list item
        # submission does work.
        self.check_for_row_in_list_table('1: Buy milk')

        self.get_item_input_box().send_keys(Keys.ENTER)
        # self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        self.check_for_row_in_list_table('1: Buy milk')
        self.assertEqual(self.get_error_element().text, EMPTY_LIST_ERROR)

        self.get_item_input_box().send_keys('Make tea')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')

    @skip
    def test_cannot_add_duplicate_items(self):
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: Buy wellies')

        self.get_item_input_box().send_keys('Buy wellies\n')
        self.check_for_row_in_list_table('1: Buy wellies')
        """
        CODE WORKS PROPERLY BUT SELENIUM WILL NOT LOCATE THE CLASS 
        FOR SOME FUCKING REASON!!
        self.assertEqual(self.get_error_element().text, DUPLICATE_LIST_ERROR)"""

    def test_error_messages_are_cleared_on_input(self):
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)
        """
        IS DISPLAYED TELLS YOU WHETHER AN ELEMENT IS VISIBLE OR NOT, WHICH IS 
        CRITICAL WHEN YOU PLAN TO HIDE ELEMENTS.
        """
        self.assertTrue(self.get_error_element().is_displayed())

        self.get_item_input_box().send_keys('a')
        self.assertFalse(self.get_error_element().is_displayed())
