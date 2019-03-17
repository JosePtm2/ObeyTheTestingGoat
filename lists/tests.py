from django.test import TestCase
from lists.models import Item


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': 'A new Item'})
        self.assertIn('A new Item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')


class ItemModelTest(TestCase):

    def create_a_new_item(self, item_text):
        item = Item()
        item.text = item_text
        item.save()

    def test_saving_and_retrieving_items(self):
        self.create_a_new_item('The first EVAH')
        self.create_a_new_item('The second')

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first = saved_items[0]
        second = saved_items[1]

        self.assertEquals(first.text, 'The first EVAH')
        self.assertEquals(second.text, 'The second')
