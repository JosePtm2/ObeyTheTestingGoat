from selenium import webdriver
import unittest


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
        self.fail('Finish the Test!')

        # She is invited to enter a to-do item straight away

        # She types 'Buy stuff from superMarket' into a text box

        # When she hits enter, the page updates, and now the page lists
        # '1: Buy stuff from superMarket' as an item in a ToDoList

        # There is still a text box inviting her to add another item. She
        # enters 'Go to the shoe shop'

        # The page updates again, and now shows both items on her list
        # She notices that the site has generated a unique URL for her,
        # there is some explanatory text to that effect

        # She visits the provided URL and her todolist is there.

        # Satisfied she leaves.


if __name__ == '__main__':
    unittest.main(warnings='ignore')
