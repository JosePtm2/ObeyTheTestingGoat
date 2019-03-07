from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import unittest
import time


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):

        # FooName has heard about a cool new online toDoApp.
        # She opens FireFox to check out its homepage
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mention ToDoLists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a ToDo Item'
        )
        # She types 'Buy stuff from superMarket' into a text box
        inputbox.send_keys('Buy stuff from superMarket')

        # When she hits enter, the page updates, and now the page lists
        # '1: Buy stuff from superMarket' as an item in a ToDoList
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy stuff from superMarket' for row in rows)
        )
        # There is still a text box inviting her to add another item. She
        # enters 'Go to the shoe shop'
        self.fail('Finish the Test!')

        # The page updates again, and now shows both items on her list
        # She notices that the site has generated a unique URL for her,
        # there is some explanatory text to that effect

        # She visits the provided URL and her todolist is there.

        # Satisfied she leaves.


if __name__ == '__main__':
    unittest.main(warnings='ignore')
