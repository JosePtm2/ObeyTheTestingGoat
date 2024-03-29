from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time
import os

MAX_WAIT = 1


class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time()-start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):

        # FooName has heard about a cool new online toDoApp.
        # She opens FireFox to check out its homepage
        self.browser.get(self.live_server_url)

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

        self.wait_for_row_in_list_table('1: Buy stuff from superMarket')
        # There is still a text box inviting her to add another item. She
        # enters 'Go to the shoe shop'
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Go to the shoe shop')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.wait_for_row_in_list_table('1: Buy stuff from superMarket')
        self.wait_for_row_in_list_table('2: Go to the shoe shop')

        # Satisfied, she leaves.

    def test_multiple_users_can_start_lists_at_diff_URLS(self):
        # FooGirl starts a new toDo list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('This is a Test')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: This is a Test')

        # She notices that her list has an unique URL
        fooGirl_list_url = self.browser.current_url
        self.assertRegex(fooGirl_list_url, '/lists/.+')

        # Now a new user, Francis, comes along to the site

        # -------We use a new browser session to make sure that no information
        # -------of fooGirl is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the homepage. There's no sign of fooGirl's lists
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('This is a Test', page_text)
        self.assertNotIn('2: Go to the shoe shop', page_text)

        # Francis starts a new list by entering a new item.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy Milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy Milk')

        # Francis gets his own URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, fooGirl_list_url)

        # Again, there is no trace of FooGirl's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('1: Buy stuff from superMarket', page_text)
        self.assertNotIn('2: Go to the shoe shop', page_text)

        # Satisfied they leave

    def test_layout_and_styling(self):
        # Foo goes to the homepage
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # She notices the inputBoc is nicely Centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )

        # She starts a new list and sees the input is nicely
        # centered there too
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
