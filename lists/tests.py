from django.test import TestCase
from lists.models import Item


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_only_saves_items_when_needed(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        Item.objects.create(text='foo 1')
        Item.objects.create(text='foo 2')

        response = self.client.get('/lists/the-only-list/')

        self.assertContains(response, 'foo 1')
        self.assertContains(response, 'foo 2')


class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new/', data={'item_text': 'A new list Item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list Item')

    def test_redirect_after_POST(self):
        response = self.client.post('/lists/new/',
                                    data={'item_text': 'A new list Item'})
        self.assertRedirects(response, '/lists/the-only-list/')


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

        self.assertEqual(first.text, 'The first EVAH')
        self.assertEqual(second.text, 'The second')
